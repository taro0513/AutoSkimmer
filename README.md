## 版本
Coding Language: python3.11
OS: win11

### 前置工作
1. `pip install -r requirements.txt`

2. 運行 database.py 進行 ORM migration

3. 設定 obs.py 的 exe_path

4. 設定 webex.py 的 exe_path

5. 設定 zoom.py 的 exe_path

6. 啟動 OBS 的 Websocket server，並取消驗證，以及設定 port 為 4455

7. 新增 OBS scene `AutoSkimmer` 並新增來源(顯示器擷取) `Scene`

8. 設定 ui/Main.py 的 `API_URL`

### 檢查
1. 運行 obs.py 看能否正常工作 (啟動 -> 開始錄影 -> 結束錄影)

2. 運行 webex.py 看能否正常工作 (啟動 -> 加入會議 -> 填寫會議ID -> 準備加入 -> 變成全螢幕 -> 設定 layout -> 設定 layout 細節 -> 開啟聊天室窗 -> 將聊天室窗變成談窗模式)

3. 運行 zoom.py 看能否正常工作 (啟動 -> 加入會議 -> 填寫會議ID&名稱 -> 變成全螢幕 -> 設定 layout -> 設定 layout 細節 -> 開啟聊天室窗 -> 將聊天室窗變成談窗模式 -> 移動聊天室窗至左邊)

### 調整
1. WebexClient(webex.py) 的 HIDE_NO_VIDEO_PEOPLE_BUTTON_X_OFFSET ，欄位中心到按鈕的偏移

2. 啟動時機跟下一步驟的等待時間

## 啟動

在 AutoSkimmer 資料夾下

1. 啟動後端服務 `fastapi run main.py`

2. 啟動 UI `streamlit run ui/Main.py`

