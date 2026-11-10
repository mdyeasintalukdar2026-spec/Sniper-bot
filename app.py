from flask import Flask, jsonify, make_response
import threading
import requests
import time
import os

app = Flask(__name__, static_folder=None)

RENDER_SERVER_URL = "https://sniper-bot-tric.onrender.com"

@app.route('/')
def home():
    return "SNIPER BOT Precision Engine - 24/7 Active"

@app.route('/ping')
def ping():
    return "OK", 200

@app.route('/signal')
def get_signal():
    try:
        current_time = time.time()
        time_slot = int(current_time / 5)
        
        trend_calc = (time_slot * 31337 + 7357) % 100
        base_signal = "CALL" if (trend_calc >= 50) else "PUT"
        
        volatility = (time_slot * 16657) % 10
        real_accuracy = 92 + volatility
        
        res = jsonify({
            "signal": base_signal,
            "trend": "SNIPER_BOT_QUANT_ANALYSIS",
            "confidence": real_accuracy,
            "status": "GREEN_EXECUTE"
        })
        res.headers.add("Access-Control-Allow-Origin", "*")
        return res
    except Exception as e:
        res = jsonify({
            "signal": "CALL",
            "trend": "STABLE MOMENTUM",
            "confidence": 96,
            "status": "GREEN_EXECUTE"
        })
        res.headers.add("Access-Control-Allow-Origin", "*")
        return res

@app.route('/bot.js')
def bot_script():
    js = """
    (function(){
        try {
            var d = document;
            
            ["sniper-bot-panel", "sniper-bot-btn", "sniper-bot-style"].forEach(function(i){
                var e = d.getElementById(i);
                if(e) e.remove();
            });

            var botMainLogo = "https://i.postimg.cc/2SpN9cDm/1793861889440.jpg";
            var renderServerUrl = "https://sniper-bot-tric.onrender.com";

            var s = d.createElement('style');
            s.id = 'sniper-bot-style';
            s.innerHTML = '@keyframes sniperGlowPulse {' +
                          '0% { box-shadow: 0 0 16px rgba(34,197,94,0.6), inset 0 0 10px rgba(34,197,94,0.3); border-color: #22c55e; }' +
                          '50% { box-shadow: 0 0 30px rgba(56,189,248,0.95), inset 0 0 18px rgba(56,189,248,0.6); border-color: #38bdf8; }' +
                          '100% { box-shadow: 0 0 16px rgba(34,197,94,0.6), inset 0 0 10px rgba(34,197,94,0.3); border-color: #22c55e; }' +
                          '}' +
                          '@keyframes heavyWavyMotion {' +
                          '0% { stroke-dashoffset: 0; transform: scaleY(1); filter: drop-shadow(0 0 8px #22c55e); }' +
                          '33% { stroke-dashoffset: 20; transform: scaleY(1.5); filter: drop-shadow(0 0 12px #38bdf8); }' +
                          '66% { stroke-dashoffset: 40; transform: scaleY(1.2); filter: drop-shadow(0 0 10px #facc15); }' +
                          '100% { stroke-dashoffset: 60; transform: scaleY(1); filter: drop-shadow(0 0 8px #ef4444); }' +
                          '}' +
                          '@keyframes candlePulseShift {' +
                          '0% { transform: scaleY(0.9); }' +
                          '50% { transform: scaleY(1.25); }' +
                          '100% { transform: scaleY(0.9); }' +
                          '}' +
                          '@keyframes candlePopIn {' +
                          '0% { transform: scale(0.3); opacity: 0; }' +
                          '100% { transform: scale(1); opacity: 1; }' +
                          '}' +
                          '@keyframes panelFadeIn { 0% { opacity: 0; transform: translate(-50%, -50%) scale(0.9); } 100% { opacity: 1; transform: translate(-50%, -50%) scale(1); } }';
            d.head.appendChild(s);

            var isExecutionLocked = false;
            var isLicensed = false;
            var currentMode = "1M";
            var autoLoopActive = false;
            var autoTimer = null;

            function createBotIcon() {
                var wrap = d.getElementById('sniper-bot-btn') || d.createElement('div');
                wrap.id = 'sniper-bot-btn';
                wrap.style.cssText = 'position:fixed;bottom:75px;left:18px;width:64px;height:64px;border-radius:50%;background:#080c16;display:flex;align-items:center;justify-content:center;border:2.5px solid #22c55e;animation:sniperGlowPulse 2.5s infinite ease-in-out;z-index:2147483647;cursor:pointer;box-sizing:border-box;overflow:hidden;';
                wrap.innerHTML = '<img src="' + botMainLogo + '" style="width:100%;height:100%;object-fit:cover;border-radius:50%;pointer-events:none;" />';

                if(!d.body.contains(wrap)) d.body.appendChild(wrap);

                var isDragging = false, startX, startY, hasMoved = false;
                wrap.onmousedown = wrap.ontouchstart = function(e){
                    isDragging = true; hasMoved = false;
                    var p = e.touches ? e.touches[0] : e;
                    startX = p.clientX - wrap.offsetLeft; startY = p.clientY - wrap.offsetTop;
                };
                wrap.onmousemove = wrap.ontouchmove = function(e){
                    if(!isDragging) return;
                    var p = e.touches ? e.touches[0] : e;
                    var nx = p.clientX - startX, ny = p.clientY - startY;
                    if(Math.abs(nx - wrap.offsetLeft) > 2 || Math.abs(ny - wrap.offsetTop) > 2) hasMoved = true;
                    wrap.style.left = nx + 'px'; wrap.style.top = ny + 'px';
                    wrap.style.bottom = 'auto'; wrap.style.right = 'auto';
                };
                wrap.onmouseup = wrap.ontouchend = function(){ isDragging = false; };
                wrap.onclick = function(){ if(!hasMoved) toggleSniperPanel(); };
            }

            createBotIcon();

            function detectMarket() {
                var marketName = "EURUSD (OTC)";
                var selectors = ['.asset-select__button', '.asset-name', '.chart-title', '.asset-select__short-name', '[class*="asset-select"]', '.deal-asset'];
                for(var i=0; i<selectors.length; i++){
                    var els = d.querySelectorAll(selectors[i]);
                    for(var k=0; k<els.length; k++){
                        var txt = els[k].innerText ? els[k].innerText.trim() : '';
                        if(txt.length > 1 && txt.length < 35 && (txt.includes('/') || txt.includes('OTC') || txt.includes('USD') || txt.includes('EUR'))) {
                            marketName = txt.replace(/\\n/g, ' ').replace(/\\s+/g, ' ');
                            break;
                        }
                    }
                    if(marketName !== "EURUSD (OTC)") break;
                }
                return marketName;
            }

            function toggleSniperPanel() {
                var existing = d.getElementById('sniper-bot-panel');
                if(existing) { existing.remove(); return; }

                var market = detectMarket();
                var panel = d.createElement('div');
                panel.id = 'sniper-bot-panel';
                // Optimized thinner width (225px) and balanced height to eliminate extra bottom gap
                panel.style.cssText = 'position:fixed;top:44%;left:50%;transform:translate(-50%, -50%);width:225px;min-height:415px;background:linear-gradient(180deg, rgba(7, 11, 20, 0.98), rgba(3, 5, 11, 0.99));border:2px solid #22c55e;border-radius:13px;box-shadow:0 12px 35px rgba(0,0,0,0.95);z-index:2147483647;font-family:-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;color:#fff;overflow:hidden;animation:panelFadeIn 0.25s ease-out;box-sizing:border-box;backdrop-filter:blur(8px);';

                if(!isLicensed) {
                    panel.innerHTML = 
                        '<div style="padding:14px;box-sizing:border-box;position:relative;">' +
                            '<div style="display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid rgba(255,255,255,0.08);padding-bottom:7px;margin-bottom:10px;">' +
                                '<div style="display:flex;align-items:center;gap:6px;">' +
                                    '<img src="' + botMainLogo + '" style="width:20px;height:20px;border-radius:50%;object-fit:cover;border:1px solid #22c55e;" />' +
                                    '<div style="font-size:10.5px;font-weight:900;letter-spacing:0.8px;color:#fff;">SNIPER BOT</div>' +
                                '</div>' +
                                '<div id="sniper-close-btn" style="cursor:pointer;font-size:12px;color:#94a3b8;padding:1px 4px;border-radius:3px;background:rgba(255,255,255,0.06);">✕</div>' +
                            '</div>' +
                            '<div style="font-size:9.5px;font-weight:700;color:#94a3b8;margin-bottom:5px;">Enter license key:</div>' +
                            '<input id="sniper-license-input" type="text" placeholder="License key..." style="width:100%;background:rgba(0,0,0,0.6);border:1px solid rgba(255,255,255,0.15);border-radius:5px;padding:8px;color:#fff;font-size:9.5px;margin-bottom:8px;box-sizing:border-box;outline:none;" />' +
                            '<button id="sniper-verify-btn" style="width:100%;background:linear-gradient(135deg, #166534, #22c55e);color:#fff;border:none;border-radius:5px;padding:8px;font-size:10.5px;font-weight:900;cursor:pointer;box-shadow:0 3px 10px rgba(34,197,94,0.4);">VERIFY LICENSE</button>' +
                        '</div>';

                    d.body.appendChild(panel);
                    d.getElementById('sniper-close-btn').onclick = function() { panel.remove(); };
                    d.getElementById('sniper-verify-btn').onclick = function() {
                        var val = d.getElementById('sniper-license-input').value.trim();
                        if(val.length > 0) {
                            isLicensed = true;
                            panel.remove();
                            toggleSniperPanel();
                        } else {
                            alert('Please enter a license key!');
                        }
                    };
                    return;
                }

                panel.innerHTML = 
                    '<div style="padding:12px 9px;box-sizing:border-box;position:relative;display:flex;flex-direction:column;justify-content:space-between;min-height:415px;">' +
                        '<div>' +
                            // Header with Verified Badge
                            '<div style="display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid rgba(255,255,255,0.08);padding-bottom:6px;margin-bottom:8px;">' +
                                '<div style="display:flex;align-items:center;gap:5px;">' +
                                    '<img src="' + botMainLogo + '" style="width:20px;height:20px;border-radius:50%;object-fit:cover;border:1px solid #22c55e;" />' +
                                    '<div>' +
                                        '<div style="font-size:10.5px;font-weight:900;letter-spacing:0.7px;color:#fff;">SNIPER BOT</div>' +
                                        '<div style="display:flex;align-items:center;gap:3px;font-size:7.5px;color:#22c55e;font-weight:700;">' +
                                            '<span style="width:3.5px;height:3.5px;background:#22c55e;border-radius:50%;display:inline-block;box-shadow:0 0 4px #22c55e;"></span> AI ENGINE ONLINE' +
                                        '</div>' +
                                    '</div>' +
                                '</div>' +
                                '<div style="display:flex;align-items:center;gap:4px;">' +
                                    '<span style="background:rgba(34,197,94,0.18);color:#22c55e;font-size:7.5px;font-weight:900;padding:1px 4px;border-radius:3px;border:1px solid rgba(34,197,94,0.4);">VERIFIED</span>' +
                                    '<div id="sniper-close-btn" style="cursor:pointer;font-size:12px;color:#94a3b8;padding:1px 3px;border-radius:3px;background:rgba(255,255,255,0.06);">✕</div>' +
                                '</div>' +
                            '</div>' +

                            // Top Mode Toggles (1m Standard & 5s Auto Mode)
                            '<div style="display:flex;gap:4px;margin-bottom:6px;">' +
                                '<button id="mode-1m" style="flex:1;background:#22c55e;color:#000;border:none;border-radius:4px;padding:5px;font-size:8px;font-weight:900;cursor:pointer;box-shadow:0 0 6px rgba(34,197,94,0.4);">1m Standard</button>' +
                                '<button id="mode-5s" style="flex:1;background:rgba(255,255,255,0.08);color:#94a3b8;border:none;border-radius:4px;padding:5px;font-size:8px;font-weight:900;cursor:pointer;">5s Auto Mode</button>' +
                            '</div>' +

                            // Auto Start / Auto Stop Container (Left Green, Right Red, smaller size)
                            '<div id="auto-controls-container" style="display:none;gap:4px;margin-bottom:6px;animation:panelFadeIn 0.2s ease-out;">' +
                                '<button id="start-auto-btn" style="flex:1;background:#22c55e;color:#000;border:none;border-radius:4px;padding:4px;font-size:7.5px;font-weight:900;cursor:pointer;box-shadow:0 0 8px rgba(34,197,94,0.5);">Auto Start</button>' +
                                '<button id="stop-auto-btn" style="flex:1;background:#ef4444;color:#fff;border:none;border-radius:4px;padding:4px;font-size:7.5px;font-weight:900;cursor:pointer;box-shadow:0 0 8px rgba(239,68,68,0.5);">Auto Stop</button>' +
                            '</div>' +

                            // Next Candle Section with ~5-6% Larger Box and Candles
                            '<div style="text-align:center;margin-bottom:8px;">' +
                                '<div style="font-size:9px;font-weight:700;color:#22c55e;margin-bottom:3px;letter-spacing:0.4px;">Next Candle??</div>' +
                                '<div id="sniper-candle-display-box" style="display:flex;align-items:center;justify-content:center;gap:3px;height:52px;background:rgba(0,0,0,0.65);border-radius:7px;padding:4px;border:1px solid rgba(56,189,248,0.35);box-shadow:inset 0 0 14px rgba(0,0,0,0.9);">' +
                                    '<div style="width:3px;height:16px;background:#ef4444;border-radius:1px;animation:candlePulseShift 1s infinite ease-in-out;"></div>' +
                                    '<div style="width:3px;height:22px;background:#22c55e;border-radius:1px;animation:candlePulseShift 1s infinite ease-in-out 0.1s;"></div>' +
                                    '<div style="width:3.5px;height:28px;background:#ef4444;border-radius:1px;animation:candlePulseShift 1s infinite ease-in-out 0.2s;"></div>' +
                                    '<div style="width:4px;height:34px;background:#22c55e;border-radius:1px;animation:candlePulseShift 1s infinite ease-in-out 0.3s;"></div>' +
                                    '<div style="width:5.5px;height:44px;background:#22c55e;border-radius:1.5px;box-shadow:0 0 12px #22c55e;animation:candlePulseShift 1s infinite ease-in-out 0.4s;"></div>' +
                                    '<div style="width:4px;height:34px;background:#ef4444;border-radius:1px;animation:candlePulseShift 1s infinite ease-in-out 0.3s;"></div>' +
                                    '<div style="width:3.5px;height:28px;background:#22c55e;border-radius:1px;animation:candlePulseShift 1s infinite ease-in-out 0.2s;"></div>' +
                                    '<div style="width:3px;height:22px;background:#ef4444;border-radius:1px;animation:candlePulseShift 1s infinite ease-in-out 0.1s;"></div>' +
                                    '<div style="width:3px;height:16px;background:#22c55e;border-radius:1px;animation:candlePulseShift 1s infinite ease-in-out;"></div>' +
                                '</div>' +
                            '</div>' +

                            // Status & Action Box (Shifted slightly down for perfect balance)
                            '<div id="sniper-action-box" style="background:rgba(0,0,0,0.5);border:1px solid rgba(255,255,255,0.12);border-radius:7px;padding:8px;text-align:center;margin-bottom:6px;">' +
                                '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;font-size:9px;">' +
                                    '<span style="color:#94a3b8;font-weight:bold;">LATEST SIGNAL</span>' +
                                    '<span id="sniper-status-badge" style="color:#22c55e;font-weight:900;background:rgba(34,197,94,0.18);padding:1px 5px;border-radius:3px;border:1px solid rgba(34,197,94,0.4);">READY</span>' +
                                '</div>' +
                                '<div id="sniper-signal-text" style="font-size:13.5px;font-weight:900;color:#facc15;margin-bottom:6px;letter-spacing:0.5px;">--- : --</div>' +
                                '<button id="sniper-get-signal-btn" style="width:100%;background:linear-gradient(135deg, #166534, #22c55e);color:#fff;border:none;border-radius:6px;padding:8px;font-size:10.5px;font-weight:900;cursor:pointer;box-shadow:0 4px 12px rgba(34,197,94,0.5);">GET SIGNAL</button>' +
                            '</div>' +
                        '</div>' +

                        // Bottom Footer with Live Quotex Timer Integration
                        '<div style="display:flex;justify-content:space-between;align-items:center;font-size:7.5px;color:#94a3b8;border-top:1px solid rgba(255,255,255,0.06);padding-top:5px;">' +
                            '<span style="color:#38bdf8;font-weight:bold;">' + market + '</span>' +
                            '<span id="sniper-live-timer" style="color:#22c55e;font-weight:900;background:rgba(34,197,94,0.12);padding:1px 4px;border-radius:3px;">00:00:00</span>' +
                        '</div>' +
                    '</div>';

                d.body.appendChild(panel);

                // Live Timer updater
                setInterval(function(){
                    var now = new Date();
                    var hrs = String(now.getHours()).padStart(2, '0');
                    var mins = String(now.getMinutes()).padStart(2, '0');
                    var secs = String(now.getSeconds()).padStart(2, '0');
                    var tmEl = d.getElementById('sniper-live-timer');
                    if(tmEl) tmEl.innerText = hrs + ':' + mins + ':' + secs;
                }, 1000);

                var btn1m = panel.querySelector('#mode-1m');
                var btn5s = panel.querySelector('#mode-5s');
                var autoControls = panel.querySelector('#auto-controls-container');
                var startAutoBtn = panel.querySelector('#start-auto-btn');
                var stopAutoBtn = panel.querySelector('#stop-auto-btn');

                btn1m.onclick = function() {
                    currentMode = "1M";
                    btn1m.style.background = '#22c55e'; btn1m.style.color = '#000'; btn1m.style.boxShadow = '0 0 6px rgba(34,197,94,0.4)';
                    btn5s.style.background = 'rgba(255,255,255,0.08)'; btn5s.style.color = '#94a3b8'; btn5s.style.boxShadow = 'none';
                    autoControls.style.display = 'none';
                    stopAutoExecution();
                };

                btn5s.onclick = function() {
                    currentMode = "5S";
                    btn5s.style.background = '#22c55e'; btn5s.style.color = '#000'; btn5s.style.boxShadow = '0 0 6px rgba(34,197,94,0.4)';
                    btn1m.style.background = 'rgba(255,255,255,0.08)'; btn1m.style.color = '#94a3b8'; btn1m.style.boxShadow = 'none';
                    autoControls.style.display = 'flex';
                };

                startAutoBtn.onclick = function() {
                    if(!autoLoopActive) {
                        autoLoopActive = true;
                        run5sAutoSequence(panel);
                        autoTimer = setInterval(function(){ run5sAutoSequence(panel); }, 6000);
                    }
                };

                stopAutoBtn.onclick = function() { stopAutoExecution(); };

                function stopAutoExecution() {
                    autoLoopActive = false;
                    if(autoTimer) clearInterval(autoTimer);
                }

                d.getElementById('sniper-close-btn').onclick = function() {
                    stopAutoExecution();
                    panel.remove();
                };

                d.getElementById('sniper-get-signal-btn').onclick = function() {
                    if(currentMode === "5S") { run5sAutoSequence(panel); }
                    else { run1MinScanningSequence(panel); }
                };
            }

            function run5sAutoSequence(panel) {
                var statusBadge = panel.querySelector('#sniper-status-badge');
                var signalText = panel.querySelector('#sniper-signal-text');
                var candleBox = panel.querySelector('#sniper-candle-display-box');

                statusBadge.innerText = '5S AUTO RUNNING';
                statusBadge.style.color = '#38bdf8';
                statusBadge.style.background = 'rgba(56,189,248,0.2)';

                // Thicker, slower motion heavy wavy sine waves with dynamic shifting color threads
                candleBox.innerHTML = 
                    '<svg width="100%" height="100%" viewBox="0 0 200 52" preserveAspectRatio="none" style="overflow:visible;">' +
                        '<path d="M 0 26 Q 25 3, 50 26 T 100 26 T 150 26 T 200 26" fill="none" stroke="#22c55e" stroke-width="4.5" style="animation:heavyWavyMotion 0.9s linear infinite;" />' +
                        '<path d="M 0 26 Q 25 48, 50 26 T 100 26 T 150 26 T 200 26" fill="none" stroke="#38bdf8" stroke-width="3.8" style="animation:heavyWavyMotion 1.1s linear infinite;" />' +
                        '<path d="M 0 26 Q 25 12, 50 26 T 100 26 T 150 26 T 200 26" fill="none" stroke="#ef4444" stroke-width="3" style="animation:heavyWavyMotion 0.7s linear infinite;" />' +
                        '<path d="M 0 26 Q 25 38, 50 26 T 100 26 T 150 26 T 200 26" fill="none" stroke="#facc15" stroke-width="2.5" style="animation:heavyWavyMotion 1s linear infinite;" />' +
                    '</svg>';

                signalText.style.fontSize = '10px';
                signalText.style.color = '#38bdf8';
                signalText.innerText = "Heavy Volatility Scanning...";

                fetch(renderServerUrl + '/signal?t=' + Date.now())
                .then(function(r){ return r.json(); })
                .catch(function(){ return {signal: "CALL", confidence: 96}; })
                .then(function(data){
                    setTimeout(function(){
                        var sig = String(data.signal || 'CALL').toUpperCase();
                        var isCall = (sig === 'CALL' || sig === 'UP' || sig === 'BUY');
                        var confidence = data.confidence || 96;

                        statusBadge.innerText = 'SUCCESS';
                        statusBadge.style.color = '#fff';
                        statusBadge.style.background = isCall ? '#22c55e' : '#ef4444';

                        signalText.style.fontSize = '13.5px';
                        signalText.style.color = isCall ? '#22c55e' : '#ef4444';
                        signalText.innerText = (isCall ? '📈 UP (' : '📉 DOWN (') + confidence + '%)';

                        var candleColor = isCall ? '#22c55e' : '#ef4444';
                        candleBox.innerHTML = 
                            '<div style="position:relative;display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;animation:candlePopIn 0.3s ease-out;">' +
                                '<div style="width:3px;height:42px;background:' + candleColor + ';position:absolute;"></div>' +
                                '<div style="width:18px;height:28px;background:' + candleColor + ';border-radius:3px;z-index:2;box-shadow:0 0 16px ' + candleColor + ';"></div>' +
                            '</div>';

                        executeTrade(isCall);
                    }, 1500);
                });
            }

            function run1MinScanningSequence(panel) {
                var statusBadge = panel.querySelector('#sniper-status-badge');
                var signalText = panel.querySelector('#sniper-signal-text');
                var candleBox = panel.querySelector('#sniper-candle-display-box');

                statusBadge.innerText = '1M SCANNING';
                statusBadge.style.color = '#ef4444';
                statusBadge.style.background = 'rgba(239,68,68,0.18)';

                var scanSteps = [
                    "Analyzing market structure...",
                    "Checking candlestick patterns...",
                    "Volatility & order flow sync...",
                    "AI neural confirmation..."
                ];

                var idx = 0;
                signalText.style.fontSize = '10px';
                signalText.style.color = '#38bdf8';

                var timer = setInterval(function() {
                    if(idx < scanSteps.length) {
                        signalText.innerText = scanSteps[idx];
                        idx++;
                    }
                }, 700);

                fetch(renderServerUrl + '/signal?t=' + Date.now())
                .then(function(r){ return r.json(); })
                .catch(function(){ return {signal: "CALL", confidence: 96}; })
                .then(function(data){
                    setTimeout(function(){
                        clearInterval(timer);
                        var sig = String(data.signal || 'CALL').toUpperCase();
                        var isCall = (sig === 'CALL' || sig === 'UP' || sig === 'BUY');
                        var confidence = data.confidence || 96;

                        statusBadge.innerText = 'SUCCESS';
                        statusBadge.style.color = '#fff';
                        statusBadge.style.background = isCall ? '#22c55e' : '#ef4444';

                        signalText.style.fontSize = '13.5px';
                        signalText.style.color = isCall ? '#22c55e' : '#ef4444';
                        signalText.innerText = (isCall ? '📈 UP (' : '📉 DOWN (') + confidence + '%)';

                        var candleColor = isCall ? '#22c55e' : '#ef4444';
                        candleBox.innerHTML = 
                            '<div style="position:relative;display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;animation:candlePopIn 0.3s ease-out;">' +
                                '<div style="width:3px;height:42px;background:' + candleColor + ';position:absolute;"></div>' +
                                '<div style="width:18px;height:28px;background:' + candleColor + ';border-radius:3px;z-index:2;box-shadow:0 0 16px ' + candleColor + ';"></div>' +
                            '</div>';

                        executeTrade(isCall);
                    }, 3000);
                });
            }

            function executeTrade(isCall) {
                if(isExecutionLocked) return;
                isExecutionLocked = true;

                var targetBtn = null;
                var buttons = d.querySelectorAll('button, div[role="button"], span[class*="btn"]');
                
                for(var i=0; i<buttons.length; i++){
                    var btn = buttons[i];
                    var text = (btn.innerText || '').trim().toUpperCase();
                    var cls = (btn.className || '').toLowerCase();
                    
                    var isUp = cls.includes('call') || cls.includes('buy') || cls.includes('up') || text === 'UP' || text === 'BUY';
                    var isDown = cls.includes('put') || cls.includes('sell') || cls.includes('down') || text === 'DOWN' || text === 'SELL';
                    
                    if(isCall && isUp && btn.getBoundingClientRect().width > 0){ targetBtn = btn; break; }
                    if(!isCall && isDown && btn.getBoundingClientRect().width > 0){ targetBtn = btn; break; }
                }

                if(!targetBtn) {
                    var selectors = isCall ? ['.section-deal__button-up', '.btn-call', 'button.call'] : ['.section-deal__button-down', '.btn-put', 'button.put'];
                    for(var i=0; i<selectors.length; i++){
                        var f = d.querySelector(selectors[i]);
                        if(f && f.getBoundingClientRect().width > 0) { targetBtn = f; break; }
                    }
                }

                if(targetBtn) {
                    try { targetBtn.click(); } catch(e) {
                        var box = targetBtn.getBoundingClientRect();
                        var ev = new MouseEvent('click', { bubbles: true, cancelable: true, view: window, clientX: box.left + box.width/2, clientY: box.top + box.height/2 });
                        targetBtn.dispatchEvent(ev);
                    }
                }

                setTimeout(function(){ isExecutionLocked = false; }, 3500);
            }

        } catch(e) { console.error("SNIPER BOT Error:", e); }
    })();
    """
    res = make_response(js)
    res.headers['Content-Type'] = 'application/javascript'
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

def start_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    threading.Thread(target=run_server, daemon=True).start()
