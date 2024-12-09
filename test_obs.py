import obsws_python as obs

# OBS WebSocket Client Initialization
cl = obs.ReqClient(host='localhost', port=4455, password='your_password_here')

# Define the scene and source details
SCENE_NAME = "李育衡的個人會議室"
SOURCE_NAME = "CiscoCollabHost.exe"
WINDOW_TITLE = "李育衡的個人會議室"
PROCESS_NAME = "CiscoCollabHost.exe"

k = cl.get_input_kind_list(unversioned=True)
# print(k.__dict__)
d = cl.get_input_default_settings(kind='window_capture')
# print(d.default_input_settings)

# c = cl.get_input_properties_list_property_items(input_name='CiscoCollabHost.exe', prop_name='window')
# print(c.__dict__)

import obsws_python as obs

# 初始化 OBS WebSocket 客戶端
cl = obs.ReqClient(host='localhost', port=4455, password='your_password_here')

# 提取的屬性
item_value = "李育衡的個人會議室:Qt5152QWindowIcon:CiscoCollabHost.exe"
scene_name = "AutoSkimmerV2"
source_name = "CiscoCollabHost Capture"

try:
    # 創建場景
    cl.create_scene(name=scene_name)
    print(f"Scene '{scene_name}' created.")

    # 創建來源，並將窗口屬性設置為提取的 item_value
    cl.create_input(
        sceneName=scene_name,
        inputName=source_name,
        inputKind="window_capture",
        inputSettings={
            "window": item_value
        },
        sceneItemEnabled=True
    )
    print(f"Source '{source_name}' added to scene '{scene_name}'.")

    # 設置為當前場景
    cl.set_current_program_scene(name=scene_name)
    print(f"Scene '{scene_name}' set as active scene.")
except Exception as e:
    print(e)


# try:
#     # Create the scene
#     cl.create_scene(name=SCENE_NAME)
#     print(f"Scene '{SCENE_NAME}' created.")


#     # Add the window capture source to the scene
#     cl.create_input(
#         sceneName=SCENE_NAME,
#         inputName=SOURCE_NAME,
#         inputKind="window_capture",
#         inputSettings={
#             "Window": f"{PROCESS_NAME}:{WINDOW_TITLE}"
#         },
#         sceneItemEnabled=True
#     )
#     print(f"Source '{SOURCE_NAME}' added to scene '{SCENE_NAME}'.")

#     # Set the active scene
#     cl.set_current_program_scene(name=SCENE_NAME)
#     print(f"Scene '{SCENE_NAME}' set as active scene.")

#     # Start recording
#     # cl.start_record()
#     print("Recording started.")

# except Exception as e:
#     print(f"An error occurred: {e}")
