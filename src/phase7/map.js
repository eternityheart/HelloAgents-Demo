/**
 * 时空地图 - 高德地图集成 (修复版)
 * 修复: 定位问题, 地图样式, 路线输入
 */

// ===== 全局变量 =====
let map = null;
let markers = [];
let polyline = null;
let markerCluster = null;
let userLocation = null;
let startMarker = null;
let endMarker = null;

// ===== DOM 元素 =====
const currentLocationEl = document.getElementById('currentLocation');
const poiListEl = document.getElementById('poiList');
const totalPoisEl = document.getElementById('totalPois');
const totalDistanceEl = document.getElementById('totalDistance');
const mapSearchEl = document.getElementById('mapSearch');
const drawRouteBtnEl = document.getElementById('drawRouteBtn');
const mapLogEl = document.getElementById('mapLog');
const startInputEl = document.getElementById('startInput');
const endInputEl = document.getElementById('endInput');

// ===== 工具函数 =====
function addLog(text) {
    if (!mapLogEl) return;
    const li = document.createElement('li');
    li.textContent = text;
    mapLogEl.insertBefore(li, mapLogEl.firstChild);
    // 限制日志数量
    if (mapLogEl.children.length > 20) {
        mapLogEl.removeChild(mapLogEl.lastChild);
    }
}

// ===== 初始化地图 =====
function initMap() {
    addLog('正在初始化地图...');

    map = new AMap.Map('amapContainer', {
        zoom: 14,
        center: [116.364, 39.966], // 默认学院南路附近
        // 使用标准地图样式 (不再使用 dark)
        mapStyle: 'amap://styles/normal',
        viewMode: '2D'
    });

    // 添加控件
    map.addControl(new AMap.Scale());
    map.addControl(new AMap.ToolBar({ position: 'RB' }));

    addLog('地图初始化完成');

    // 初始化定位 (带 fallback)
    initGeolocation();

    // 从 localStorage 加载之前的搜索结果 (如果有)
    loadCachedPois();
}

// ===== 定位功能 (带 fallback) =====
function initGeolocation() {
    addLog('正在获取定位...');

    // 检测是否为 file:// 协议
    if (window.location.protocol === 'file:') {
        addLog('本地文件模式，使用默认位置');
        setDefaultLocation();
        return;
    }

    // 尝试浏览器原生定位
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                userLocation = [position.coords.longitude, position.coords.latitude];
                updateLocationDisplay('当前位置', userLocation);
                addUserMarker(userLocation);
                map.setCenter(userLocation);
                addLog('定位成功');
            },
            (error) => {
                addLog(`定位失败: ${error.message}`);
                setDefaultLocation();
            },
            { timeout: 5000, enableHighAccuracy: true }
        );
    } else {
        setDefaultLocation();
    }
}

// ===== 设置默认位置 =====
function setDefaultLocation() {
    // 默认位置: 学院南路 38号 (北京)
    userLocation = [116.364, 39.966];
    updateLocationDisplay('学院南路 (默认)', userLocation);
    addUserMarker(userLocation);
    map.setCenter(userLocation);
}

// ===== 更新位置显示 =====
function updateLocationDisplay(name, coords) {
    if (currentLocationEl) {
        currentLocationEl.innerHTML = `
            <div style="font-weight: 500;">📍 ${name}</div>
            <div style="font-size: 0.8rem; color: #888; margin-top: 4px;">
                ${coords[0].toFixed(4)}, ${coords[1].toFixed(4)}
            </div>
        `;
    }
}

// ===== 添加用户位置标记 =====
function addUserMarker(position) {
    if (startMarker) {
        map.remove(startMarker);
    }

    startMarker = new AMap.Marker({
        position: position,
        title: '我的位置',
        icon: new AMap.Icon({
            size: new AMap.Size(32, 32),
            image: 'https://webapi.amap.com/theme/v1.3/markers/n/mark_r.png',
            imageSize: new AMap.Size(32, 32)
        }),
        zIndex: 200,
        animation: 'AMAP_ANIMATION_DROP'
    });

    map.add(startMarker);
}

// ===== 添加 POI 标记 =====
function addPoiMarkers(pois) {
    // 清除旧标记
    if (markers.length) {
        map.remove(markers);
        markers = [];
    }
    if (markerCluster) {
        markerCluster.setMap(null);
    }

    if (!pois || pois.length === 0) {
        if (poiListEl) {
            poiListEl.innerHTML = '<div class="poi-item"><div class="name">暂无数据</div></div>';
        }
        if (totalPoisEl) totalPoisEl.textContent = '0';
        return;
    }

    // 创建标记
    let totalDist = 0;

    pois.forEach((poi, index) => {
        const lnglat = poi.location.split(',');
        const position = [parseFloat(lnglat[0]), parseFloat(lnglat[1])];

        // 使用彩色图标
        const marker = new AMap.Marker({
            position: position,
            title: poi.name,
            icon: new AMap.Icon({
                size: new AMap.Size(28, 32),
                image: 'https://webapi.amap.com/theme/v1.3/markers/n/mark_b.png',
                imageSize: new AMap.Size(28, 32)
            }),
            label: {
                content: `<div style="background:#00a0e9;color:#fff;padding:2px 8px;border-radius:10px;font-size:12px;font-weight:bold;box-shadow:0 2px 6px rgba(0,0,0,0.2);">${index + 1}</div>`,
                direction: 'top',
                offset: new AMap.Pixel(0, -5)
            },
            extData: poi
        });

        // 点击事件
        marker.on('click', () => {
            showPoiInfo(poi);
        });

        markers.push(marker);

        // 累计距离 (如果有 _distance 字段)
        if (poi._distance) {
            totalDist += poi._distance;
        }
    });

    // 直接添加标记 (不使用聚合，保证都能看到)
    map.add(markers);

    // 更新 POI 列表
    updatePoiList(pois);

    // 更新统计
    if (totalPoisEl) totalPoisEl.textContent = pois.length;
    if (totalDistanceEl) totalDistanceEl.textContent = totalDist.toFixed(1);

    // 自适应视野
    if (markers.length > 0) {
        map.setFitView(markers);
    }

    addLog(`已加载 ${pois.length} 个探索点`);
}

// ===== 更新 POI 列表 =====
function updatePoiList(pois) {
    if (!poiListEl) return;
    poiListEl.innerHTML = pois.map((poi, i) => `
        <div class="poi-item" onclick="focusPoi(${i})">
            <div class="name">${i + 1}. ${poi.name}</div>
            <div class="distance">${poi._distance ? poi._distance.toFixed(1) + ' km' : poi.address || ''}</div>
        </div>
    `).join('');
}

// ===== 聚焦某个 POI =====
function focusPoi(index) {
    const marker = markers[index];
    if (marker) {
        map.setCenter(marker.getPosition());
        map.setZoom(16);
        showPoiInfo(marker.getExtData());
    }
}

// ===== 显示 POI 信息窗体 =====
function showPoiInfo(poi) {
    const infoWindow = new AMap.InfoWindow({
        content: `
            <div style="padding:12px;min-width:180px;">
                <h4 style="margin:0 0 8px 0;color:#00a0e9;">${poi.name}</h4>
                <p style="margin:0;font-size:13px;color:#666;">${poi.address || '无地址'}</p>
                ${poi.biz_ext?.rating ? `<p style="margin:8px 0 0 0;font-size:13px;">⭐ ${poi.biz_ext.rating}</p>` : ''}
            </div>
        `,
        offset: new AMap.Pixel(0, -30)
    });

    const lnglat = poi.location.split(',');
    infoWindow.open(map, [parseFloat(lnglat[0]), parseFloat(lnglat[1])]);
}

// ===== 路线规划 (支持手动输入) =====
function planRoute() {
    const startAddr = startInputEl ? startInputEl.value.trim() : '';
    const endAddr = endInputEl ? endInputEl.value.trim() : '';

    if (!startAddr && !endAddr && markers.length < 2) {
        addLog('请输入起点和终点，或确保有至少2个探索点');
        return;
    }

    addLog('正在规划路线...');

    // 如果有手动输入，使用地理编码
    if (startAddr || endAddr) {
        planRouteWithAddresses(startAddr, endAddr);
    } else {
        // 使用已有的 markers
        drawPolyline(markers.map(m => m.getPosition()));
    }
}

// ===== 根据地址规划路线 =====
function planRouteWithAddresses(startAddr, endAddr) {
    const geocoder = new AMap.Geocoder({ city: '北京' });

    const startPromise = startAddr
        ? new Promise((resolve) => {
            geocoder.getLocation(startAddr, (status, result) => {
                if (status === 'complete' && result.geocodes.length) {
                    resolve(result.geocodes[0].location);
                } else {
                    resolve(userLocation ? new AMap.LngLat(userLocation[0], userLocation[1]) : null);
                }
            });
        })
        : Promise.resolve(userLocation ? new AMap.LngLat(userLocation[0], userLocation[1]) : null);

    const endPromise = endAddr
        ? new Promise((resolve) => {
            geocoder.getLocation(endAddr, (status, result) => {
                if (status === 'complete' && result.geocodes.length) {
                    resolve(result.geocodes[0].location);
                } else {
                    resolve(null);
                }
            });
        })
        : Promise.resolve(markers.length > 0 ? markers[markers.length - 1].getPosition() : null);

    Promise.all([startPromise, endPromise]).then(([startPos, endPos]) => {
        if (!startPos || !endPos) {
            addLog('无法解析起点或终点地址');
            return;
        }

        // 添加起点终点标记
        if (startMarker) map.remove(startMarker);
        if (endMarker) map.remove(endMarker);

        startMarker = new AMap.Marker({
            position: startPos,
            icon: 'https://webapi.amap.com/theme/v1.3/markers/n/start.png'
        });

        endMarker = new AMap.Marker({
            position: endPos,
            icon: 'https://webapi.amap.com/theme/v1.3/markers/n/end.png'
        });

        map.add([startMarker, endMarker]);

        // 画路线
        drawPolyline([startPos, endPos]);

        // 调整视野
        map.setFitView([startMarker, endMarker]);

        addLog(`路线: ${startAddr || '当前位置'} → ${endAddr || '目的地'}`);
    });
}

// ===== 绘制路线 (Polyline) =====
function drawPolyline(path) {
    // 清除旧路线
    if (polyline) {
        map.remove(polyline);
    }

    // 创建折线
    polyline = new AMap.Polyline({
        path: path,
        strokeColor: '#00a0e9',
        strokeWeight: 5,
        strokeOpacity: 0.9,
        strokeStyle: 'solid',
        lineJoin: 'round',
        lineCap: 'round',
        showDir: true
    });

    map.add(polyline);
    addLog('路线绘制完成');
}

// ===== 地图搜索 =====
function initSearch() {
    if (!mapSearchEl) return;

    mapSearchEl.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            const keyword = mapSearchEl.value.trim();
            if (!keyword) return;

            addLog(`搜索: ${keyword}`);

            const placeSearch = new AMap.PlaceSearch({
                city: '北京',
                pageSize: 10
            });

            placeSearch.search(keyword, (status, result) => {
                if (status === 'complete' && result.poiList) {
                    const pois = result.poiList.pois.map(p => ({
                        name: p.name,
                        address: p.address,
                        location: `${p.location.lng},${p.location.lat}`,
                        biz_ext: { rating: p.rating }
                    }));
                    addPoiMarkers(pois);

                    // 缓存结果
                    localStorage.setItem('cachedPois', JSON.stringify(pois));
                } else {
                    addLog('未找到相关地点');
                }
            });
        }
    });
}

// ===== 加载缓存的 POI =====
function loadCachedPois() {
    const cached = localStorage.getItem('cachedPois');
    if (cached) {
        try {
            const pois = JSON.parse(cached);
            if (pois.length > 0) {
                addPoiMarkers(pois);
                addLog('已加载上次探索结果');
            }
        } catch (e) {
            console.error('Failed to load cached POIs', e);
        }
    }
}

// ===== 事件绑定 =====
if (drawRouteBtnEl) {
    drawRouteBtnEl.addEventListener('click', planRoute);
}

// ===== 初始化 =====
window.onload = initMap;
initSearch();
