import subprocess
import datetime as dt

except_process_names = ["AccessibilitySettingsExtension.appex",
                        "WallpaperDynamicExtension",
                        "SoftwareUpdateSettingsExtension"]


def close_system_preferences():
    # 終了するプロセスの名前を指定
    process_names = ["Library/ExtensionKit/Extensions/"]
    kill_process_list = []
    # 例外プロセスが含まれるか判定するフラグ
    global except_flag
    except_flag = True

    for process_name in process_names:
        # psコマンドを使用してプロセスを取得し、grepコマンドを使用して該当するプロセスをフィルタリングします
        process_list = subprocess.run(
            ["ps", "aux"], capture_output=True, text=True).stdout.split("\n")
        filtered_process_list = [
            process for process in process_list if process_name in process]

        # 閉じないプロセスが含まれていないか判定
        for process in filtered_process_list:
            for name in except_process_names:
                #プロセスに例外プロセスが含まれていたらFalse
                if name in process:
                    except_flag = False
            #含まれていない場合、プロセスをKILLリストに追加
            if except_flag == True:
                kill_process_list.append(process)
            else:
                except_flag = True

        print(kill_process_list)

        # 該当するプロセスを終了します
        for process in kill_process_list:
            process_info = process.split()
            pid = process_info[1]
            subprocess.run(["kill", "-SIGKILL", pid])

now = dt.datetime.now()
real_time = f"echo '{now:%Y-%m-%d %H時%M分%S秒} kill_process.py' >> ~/documents/tools2/date.txt"
subprocess.run([real_time],shell=True)

close_system_preferences()
