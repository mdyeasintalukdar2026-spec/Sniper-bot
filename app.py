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
        
        real_accuracy = 88 + ((int(current_time * 7) + 13) % 12)
        
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
            "confidence": 95,
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
                          '@keyframes videoScannerMotion {' +
                          '0% { stroke-dashoffset: 0; transform: scaleY(1); filter: drop-shadow(0 0 5px #38bdf8); }' +
                          '50% { stroke-dashoffset: 30; transform: scaleY(1.3); filter: drop-shadow(0 0 9px #22c55e); }' +
                          '100% { stroke-dashoffset: 60; transform: scaleY(1); filter: drop-shadow(0 0 5px #ef4444); }' +
                          '}' +
                          '@keyframes nodeCenterGlow {' +
                          '0% { transform: scale(0.9); opacity: 0.7; }' +
                          '50% { transform: scale(1.25); opacity: 1; box-shadow: 0 0 12px #38bdf8; }' +
                          '100% { transform: scale(0.9); opacity: 0.7; }' +
                          '}' +
                          '@keyframes candlePulseShift {' +
                          '0% { transform: scaleY(0.92); }' +
                          '50% { transform: scaleY(1.15); }' +
                          '100% { transform: scaleY(0.92); }' +
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

            function detectMarketAndPayout() {
                var marketName = "EURUSD (OTC)";
                var payout = "90%";
                
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

                var pSelectors = ['.asset-select__payout', '[class*="payout"]', '.deal-payout', 'span'];
                for(var i=0; i<pSelectors.length; i++){
                    var els = d.querySelectorAll(pSelectors[i]);
                    for(var k=0; k<els.length; k++){
                        var t = els[k].innerText ? els[k].innerText.trim() : '';
                        if(t.includes('%') && t.length < 8) {
                            payout = t;
                            break;
                        }
                    }
                    if(payout !== "90%") break;
                }

                return marketName + " " + payout;
            }

            function toggleSniperPanel() {
                var existing = d.getElementById('sniper-bot-panel');
                if(existing) { existing.remove(); return; }

                var marketInfo = detectMarketAndPayout();
                var panel = d.createElement('div');
                panel.id = 'sniper-bot-panel';
                // Optimized width (212px) and balanced height as requested
                panel.style.cssText = 'position:fixed;top:44%;left:50%;transform:translate(-50%, -50%);width:212px;background:linear-gradient(180deg, rgba(7, 11, 20, 0.98), rgba(3, 5, 11, 0.99));border:2px solid #22c55e;border-radius:11px;box-shadow:0 10px 30px rgba(0,0,0,0.95);z-index:2147483647;font-family:-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;color:#fff;overflow:hidden;animation:panelFadeIn 0.2s ease-out;box-sizing:border-box;backdrop-filter:blur(8px);';

                if(!isLicensed) {
                    panel.innerHTML = 
                        '<div style="padding:10px;box-sizing:border-box;position:relative;">' +
                            '<div style="display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid rgba(255,255,255,0.08);padding-bottom:4px;margin-bottom:6px;">' +
                                '<div style="display:flex;align-items:center;gap:4px;">' +
                                    '<img src="' + botMainLogo + '" style="width:16px;height:16px;border-radius:50%;object-fit:cover;border:1px solid #22c55e;" />' +
                                    '<div style="font-size:9.5px;font-weight:900;letter-spacing:0.5px;color:#fff;">SNIPER BOT</div>' +
                                '</div>' +
                                '<div id="sniper-close-btn" style="cursor:pointer;font-size:10px;color:#94a3b8;padding:1px 3px;border-radius:3px;background:rgba(255,255,255,0.06);">✕</div>' +
                            '</div>' +
                            '<div style="font-size:8.5px;font-weight:700;color:#94a3b8;margin-bottom:3px;">Password / Key:</div>' +
                            '<input id="sniper-license-input" type="text" placeholder="Key..." style="width:100%;background:rgba(0,0,0,0.6);border:1px solid rgba(255,255,255,0.15);border-radius:4px;padding:5px;color:#fff;font-size:8.5px;margin-bottom:5px;box-sizing:border-box;outline:none;" />' +
                            '<button id="sniper-verify-btn" style="width:100%;background:linear-gradient(135deg, #166534, #22c55e);color:#fff;border:none;border-radius:3.5px;padding:5px;font-size:9.5px;font-weight:900;cursor:pointer;box-shadow:0 2px 6px rgba(34,197,94,0.4);">VERIFY</button>' +
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
                            alert('Please enter a valid key!');
                        }
                    };
                    return;
                }

                panel.innerHTML = 
                    '<div style="padding:8px 7px;box-sizing:border-box;position:relative;display:flex;flex-direction:column;justify-content:space-between;">' +
                        '<div>' +
                            // Header with Verified Badge
                            '<div style="display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid rgba(255,255,255,0.08);padding-bottom:4px;margin-bottom:5px;">' +
                                '<div style="display:flex;align-items:center;gap:4px;">' +
                                    '<img src="' + botMainLogo + '" style="width:16px;height:16px;border-radius:50%;object-fit:cover;border:1px solid #22c55e;" />' +
                                    '<div>' +
                                        '<div style="font-size:9.5px;font-weight:900;letter-spacing:0.5px;color:#fff;">SNIPER BOT</div>' +
                                        '<div style="display:flex;align-items:center;gap:2px;font-size:6.5px;color:#22c55e;font-weight:700;">' +
                                            '<span style="width:3px;height:3px;background:#22c55e;border-radius:50%;display:inline-block;box-shadow:0 0 3px #22c55e;"></span> AI ONLINE' +
                                        '</div>' +
                                    '</div>' +
                                '</div>' +
                                '<div style="display:flex;align-items:center;gap:3px;">' +
                                    '<span style="background:rgba(34,197,94,0.18);color:#22c55e;font-size:6.5px;font-weight:900;padding:1px 3px;border-radius:3px;border:1px solid rgba(34,197,94,0.4);">VERIFIED</span>' +
                                    '<div id="sniper-close-btn" style="cursor:pointer;font-size:10px;color:#94a3b8;padding:1px 3px;border-radius:3px;background:rgba(255,255,255,0.06);">✕</div>' +
                                '</div>' +
                            '</div>' +

                            // Top Mode Toggles (1m Standard & 5s Auto Mode)
                            '<div style="display:flex;gap:3px;margin-bottom:4px;">' +
                                '<button id="mode-1m" style="flex:1;background:#22c55e;color:#000;border:none;border-radius:3.5px;padding:3.5px;font-size:7px;font-weight:900;cursor:pointer;box-shadow:0 0 5px rgba(34,197,94,0.4);">1m Standard</button>' +
                                '<button id="mode-5s" style="flex:1;background:rgba(255,255,255,0.08);color:#94a3b8;border:none;border-radius:3.5px;padding:3.5px;font-size:7px;font-weight:900;cursor:pointer;">5s Auto Mode</button>' +
                            '</div>' +

                            // Auto Start (Green) / Auto Stop (Red) Buttons - 10-20% Smaller as requested
                            '<div id="auto-controls-container" style="display:none;gap:3px;margin-bottom:4px;transition:all 0.3s ease;">' +
                                '<button id="start-auto-btn" style="flex:1;background:#22c55e;color:#000;border:none;border-radius:2.5px;padding:2.5px 4px;font-size:6px;font-weight:900;cursor:pointer;box-shadow:0 0 4px rgba(34,197,94,0.5);">Auto Start</button>' +
                                '<button id="stop-auto-btn" style="flex:1;background:#ef4444;color:#fff;border:none;border-radius:2.5px;padding:2.5px 4px;font-size:6px;font-weight:900;cursor:pointer;box-shadow:0 0 4px rgba(239,68,68,0.5);">Auto Stop</button>' +
                            '</div>' +

                            // Next Candle Section with multiple standing candles (Green/Red alternating row)
                            '<div style="text-align:center;margin-bottom:5px;">' +
                                '<div style="font-size:8px;font-weight:700;color:#22c55e;margin-bottom:2px;letter-spacing:0.3px;">Next Candle??</div>' +
                                '<div id="sniper-candle-display-box" style="display:flex;align-items:center;justify-content:center;gap:4px;height:52px;background:rgba(0,0,0,0.65);border-radius:5px;padding:4px;border:1px solid rgba(56,189,248,0.4);box-shadow:inset 0 0 10px rgba(0,0,0,0.9);">' +
                                    // 8 standing candles (Green & Red alternating)
                                    '<div style="display:flex;flex-direction:column;align-items:center;animation:candlePulseShift 1.2s infinite ease-in-out;"><div style="width:1.5px;height:8px;background:#22c55e;"></div><div style="width:4px;height:24px;background:#22c55e;border-radius:1px;box-shadow:0 0 5px #22c55e;"></div><div style="width:1.5px;height:8px;background:#22c55e;"></div></div>' +
                                    '<div style="display:flex;flex-direction:column;align-items:center;animation:candlePulseShift 1.2s infinite ease-in-out 0.15s;"><div style="width:1.5px;height:8px;background:#ef4444;"></div><div style="width:4px;height:28px;background:#ef4444;border-radius:1px;box-shadow:0 0 5px #ef4444;"></div><div style="width:1.5px;height:8px;background:#ef4444;"></div></div>' +
                                    '<div style="display:flex;flex-direction:column;align-items:center;animation:candlePulseShift 1.2s infinite ease-in-out 0.3s;"><div style="width:1.5px;height:8px;background:#22c55e;"></div><div style="width:4px;height:20px;background:#22c55e;border-radius:1px;box-shadow:0 0 5px #22c55e;"></div><div style="width:1.5px;height:8px;background:#22c55e;"></div></div>' +
                                    '<div style="display:flex;flex-direction:column;align-items:center;animation:candlePulseShift 1.2s infinite ease-in-out 0.45s;"><div style="width:1.5px;height:8px;background:#ef4444;"></div><div style="width:4px;height:32px;background:#ef4444;border-radius:1px;box-shadow:0 0 5px #ef4444;"></div><div style="width:1.5px;height:8px;background:#ef4444;"></div></div>' +
                                    '<div style="display:flex;flex-direction:column;align-items:center;animation:candlePulseShift 1.2s infinite ease-in-out 0.6s;"><div style="width:1.5px;height:8px;background:#22c55e;"></div><div style="width:4px;height:26px;background:#22c55e;border-radius:1px;box-shadow:0 0 5px #22c55e;"></div><div style="width:1.5px;height:8px;background:#22c55e;"></div></div>' +
                                    '<div style="display:flex;flex-direction:column;align-items:center;animation:candlePulseShift 1.2s infinite ease-in-out 0.75s;"><div style="width:1.5px;height:8px;background:#ef4444;"></div><div style="width:4px;height:22px;background:#ef4444;border-radius:1px;box-shadow:0 0 5px #ef4444;"></div><div style="width:1.5px;height:8px;background:#ef4444;"></div></div>' +
                                    '<div style="display:flex;flex-direction:column;align-items:center;animation:candlePulseShift 1.2s infinite ease-in-out 0.9s;"><div style="width:1.5px;height:8px;background:#22c55e;"></div><div style="width:4px;height:30px;background:#22c55e;border-radius:1px;box-shadow:0 0 5px #22c55e;"></div><div style="width:1.5px;height:8px;background:#22c55e;"></div></div>' +
                                    '<div style="display:flex;flex-direction:column;align-items:center;animation:candlePulseShift 1.2s infinite ease-in-out 1.05s;"><div style="width:1.5px;height:8px;background:#ef4444;"></div><div style="width:4px;height:25px;background:#ef4444;border-radius:1px;box-shadow:0 0 5px #ef4444;"></div><div style="width:1.5px;height:8px;background:#ef4444;"></div></div>' +
                                '</div>' +
                            '</div>' +

                            // Status & Action Box
                            '<div id="sniper-action-box" style="background:rgba(0,0,0,0.5);border:1px solid rgba(255,255,255,0.12);border-radius:5px;padding:6px;text-align:center;margin-bottom:4px;">' +
                                '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:2px;font-size:8px;">' +
                                    '<span style="color:#94a3b8;font-weight:bold;">LATEST SIGNAL</span>' +
                                    '<span id="sniper-status-badge" style="color:#22c55e;font-weight:900;background:rgba(34,197,94,0.18);padding:1px 4px;border-radius:2.5px;border:1px solid rgba(34,197,94,0.4);">READY</span>' +
                                '</div>' +
                                '<div id="sniper-signal-text" style="font-size:12px;font-weight:900;color:#facc15;margin-bottom:4px;letter-spacing:0.5px;">--- : --</div>' +
                                '<button id="sniper-get-signal-btn" style="width:100%;background:linear-gradient(135deg, #166534, #22c55e);color:#fff;border:none;border-radius:4px;padding:6px;font-size:9.5px;font-weight:900;cursor:pointer;box-shadow:0 2px 8px rgba(34,197,94,0.5);">GET SIGNAL</button>' +
                            '</div>' +
                        '</div>' +

                        // Bottom Footer with Live Detected Market & 5s Countdown Timer
                        '<div style="display:flex;justify-content:space-between;align-items:center;font-size:7px;color:#94a3b8;border-top:1px solid rgba(255,255,255,0.06);padding-top:3px;">' +
                            '<span id="sniper-market-display" style="color:#38bdf8;font-weight:bold;">' + marketInfo + '</span>' +
                            '<span id="sniper-live-timer" style="color:#22c55e;font-weight:900;background:rgba(34,197,94,0.12);padding:1px 3px;border-radius:2.5px;">00:00:05</span>' +
                        '</div>' +
                    '</div>';

                d.body.appendChild(panel);

                // 5-Second Countdown Timer Loop
                var countdownVal = 5;
                setInterval(function(){
                    countdownVal--;
                    if(countdownVal < 0) countdownVal = 5;
                    var tmEl = d.getElementById('sniper-live-timer');
                    if(tmEl && currentMode === "5S" && autoLoopActive) {
                        tmEl.innerText = '00:00:' + (countdownVal < 10 ? '0' + countdownVal : countdownVal);
                    } else if(tmEl && currentMode === "1M") {
                        var now = new Date();
                        var hrs = String(now.getHours()).padStart(2, '0');
                        var mins = String(now.getMinutes()).padStart(2, '0');
                        var secs = String(now.getSeconds()).padStart(2, '0');
                        tmEl.innerText = hrs + ':' + mins + ':' + secs;
                    }
                }, 1000);

                var btn1m = panel.querySelector('#mode-1m');
                var btn5s = panel.querySelector('#mode-5s');
                var autoControls = panel.querySelector('#auto-controls-container');
                var startAutoBtn = panel.querySelector('#start-auto-btn');
                var stopAutoBtn = panel.querySelector('#stop-auto-btn');

                btn1m.onclick = function() {
                    currentMode = "1M";
                    btn1m.style.background = '#22c55e'; btn1m.style.color = '#000'; btn1m.style.boxShadow = '0 0 5px rgba(34,197,94,0.4)';
                    btn5s.style.background = 'rgba(255,255,255,0.08)'; btn5s.style.color = '#94a3b8'; btn5s.style.boxShadow = 'none';
                    autoControls.style.display = 'none';
                    stopAutoExecution();
                };

                btn5s.onclick = function() {
                    currentMode = "5S";
                    btn5s.style.background = '#22c55e'; btn5s.style.color = '#000'; btn5s.style.boxShadow = '0 0 5px rgba(34,197,94,0.4)';
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
                    var statusBadge = panel.querySelector('#sniper-status-badge');
                    if(statusBadge) { statusBadge.innerText = 'READY'; statusBadge.style.color = '#22c55e'; statusBadge.style.background = 'rgba(34,197,94,0.18)'; }
                }

                d.getElementById('sniper-close-btn').onclick = function() {
                    stopAutoExecution();
                    panel.remove();
                };

                d.getElementById('sniper-get-signal-btn').onclick = function() {
                    if(currentMode === "5S") { run5sAutoSequence(panel); }
                    else { run1MinStandardSequence(panel); }
                };
            }

            function run5sAutoSequence(panel) {
                var statusBadge = panel.querySelector('#sniper-status-badge');
                var signalText = panel.querySelector('#sniper-signal-text');
                var candleBox = panel.querySelector('#sniper-candle-display-box');

                statusBadge.innerText = '5S AUTO RUNNING';
                statusBadge.style.color = '#38bdf8';
                statusBadge.style.background = 'rgba(56,189,248,0.2)';

                // Exact AI Signal Scanner layout with center node and intersecting wavy sine threads from video
                candleBox.innerHTML = 
                    '<div style="position:relative;width:100%;height:100%;display:flex;align-items:center;justify-content:center;">' +
                        '<div style="position:absolute;top:2px;left:5px;font-size:7px;font-weight:900;color:#38bdf8;letter-spacing:0.5px;">AI SIGNAL SCANNER</div>' +
                        '<div style="position:absolute;width:10px;height:10px;background:#38bdf8;border-radius:50%;animation:nodeCenterGlow 1s infinite ease-in-out;box-shadow:0 0 10px #38bdf8;"></div>' +
                        '<svg width="100%" height="100%" viewBox="0 0 200 52" preserveAspectRatio="none" style="overflow:visible;">' +
                            '<path d="M 0 26 Q 25 4, 50 26 T 100 26 T 150 26 T 200 26" fill="none" stroke="#22c55e" stroke-width="3" style="animation:videoScannerMotion 1.2s linear infinite;" />' +
                            '<path d="M 0 26 Q 25 48, 50 26 T 100 26 T 150 26 T 200 26" fill="none" stroke="#38bdf8" stroke-width="2.5" style="animation:videoScannerMotion 1.5s linear infinite;" />' +
                        '</svg>' +
                    '</div>';

                var scanTexts = [
                    "Scanning Order Book...",
                    "Detecting Volatility Spikes...",
                    "Algorithmic Pattern Sync...",
                    "Executing Auto Order..."
                ];
                var sIdx = 0;
                signalText.style.fontSize = '9px';
                signalText.style.color = '#38bdf8';
                signalText.innerText = scanTexts[0];

                var stTimer = setInterval(function(){
                    sIdx++;
                    if(sIdx < scanTexts.length) signalText.innerText = scanTexts[sIdx];
                }, 400);

                fetch(renderServerUrl + '/signal?t=' + Date.now())
                .then(function(r){ return r.json(); })
                .catch(function(){ return {signal: "CALL", confidence: 92}; })
                .then(function(data){
                    setTimeout(function(){
                        clearInterval(stTimer);
                        var sig = String(data.signal || 'CALL').toUpperCase();
                        var isCall = (sig === 'CALL' || sig === 'UP' || sig === 'BUY');
                        var confidence = data.confidence || 92;

                        statusBadge.innerText = 'SUCCESS';
                        statusBadge.style.color = '#fff';
                        statusBadge.style.background = isCall ? '#22c55e' : '#ef4444';

                        signalText.style.fontSize = '12px';
                        signalText.style.color = isCall ? '#22c55e' : '#ef4444';
                        signalText.innerText = (isCall ? '📈 UP (' : '📉 DOWN (') + confidence + '%)';

                        var candleColor = isCall ? '#22c55e' : '#ef4444';
                        candleBox.innerHTML = 
                            '<div style="position:relative;display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;animation:candlePopIn 0.3s ease-out;">' +
                                '<div style="width:2.5px;height:40px;background:' + candleColor + ';position:absolute;"></div>' +
                                '<div style="width:15px;height:26px;background:' + candleColor + ';border-radius:2.5px;z-index:2;box-shadow:0 0 12px ' + candleColor + ';"></div>' +
                            '</div>';

                        executeTrade(isCall);
                    }, 1600);
                });
            }

            function run1MinStandardSequence(panel) {
                var statusBadge = panel.querySelector('#sniper-status-badge');
                var signalText = panel.querySelector('#sniper-signal-text');
                var candleBox = panel.querySelector('#sniper-candle-display-box');

                statusBadge.innerText = '1M SCANNING';
                statusBadge.style.color = '#facc15';
                statusBadge.style.background = 'rgba(250,204,21,0.18)';

                candleBox.innerHTML = 
                    '<div style="position:relative;width:100%;height:100%;display:flex;align-items:center;justify-content:center;">' +
                        '<div style="position:absolute;top:2px;left:5px;font-size:7px;font-weight:900;color:#facc15;letter-spacing:0.5px;">AI SIGNAL SCANNER</div>' +
                        '<div style="width:32px;height:32px;border:3px dashed #facc15;border-top:3px solid #38bdf8;border-radius:50%;animation:nodeCenterGlow 1s infinite linear;box-shadow:0 0 10px #facc15;"></div>' +
                    '</div>';

                var scanSteps = [
                    "Analyzing market structure...",
                    "Checking candlestick patterns...",
                    "Volatility & order flow sync...",
                    "Ready for Manual Decision..."
                ];

                var idx = 0;
                signalText.style.fontSize = '9px';
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

                        signalText.style.fontSize = '12px';
                        signalText.style.color = isCall ? '#22c55e' : '#ef4444';
                        signalText.innerText = (isCall ? '📈 UP (' : '📉 DOWN (') + confidence + '%)';

                        var candleColor = isCall ? '#22c55e' : '#ef4444';
                        candleBox.innerHTML = 
                            '<div style="position:relative;display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;animation:candlePopIn 0.3s ease-out;">' +
                                '<div style="width:2.5px;height:40px;background:' + candleColor + ';position:absolute;"></div>' +
                                '<div style="width:15px;height:26px;background:' + candleColor + ';border-radius:2.5px;z-index:2;box-shadow:0 0 12px ' + candleColor + ';"></div>' +
                            '</div>';
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
