# Black Code fomatter

## 가상 환경에서 black 설치하기

### 아직 가상 환경을 활성화하지 않았다면, 활성화하세요

Windows:

```
.venv\Scripts\activate
```

macOS와 Linux:

```
source .venv/bin/activate
```

---

### pip를 사용해 black을 설치하세요

window

```
pip_install.bat black
```

mac

```
./pip_install.sh black
```

## black을 사용하여 파이썬 코드 포맷하기

하나의 파일을 포맷하려면 다음 명령어를 실행하세요

```
black 경로/파일명.py
```

전체 프로젝트를 포맷하려면 다음 명령어를 실행하세요

```
black 프로젝트/경로
```

실행결과 EX

```
$ black .
```

```
reformatted /Users/minhyeok/Desktop/local-development/AICP-UNIST/news-crawler/src/settings.py
reformatted /Users/minhyeok/Desktop/local-development/AICP-UNIST/news-crawler/src/items.py
reformatted /Users/minhyeok/Desktop/local-development/AICP-UNIST/news-crawler/src/utils.py

All done! ✨ 🍰 ✨
3 files reformatted, 8 files left unchanged.
```

---

## Visual Studio Code에서 black 통합하기

black을 사용하여 Visual Studio Code에서 코드를 자동으로 포맷하려면 다음 단계를 따르세요

a. 아직 설치하지 않았다면, 확장 탭(Ctrl+Shift+X 또는 Cmd+Shift+X)에서 "Python"을 검색하여 Microsoft의 "Python" 확장 프로그램을 설치하세요.

b. Visual Studio Code에서 프로젝트를 여세요. 설정에 가려면 왼쪽 하단의 톱니바퀴 아이콘을 클릭한 다음 "Settings"를 선택합니다.

c. 설정 검색창에서 "python formatting provider"를 검색하여 관련 설정을 찾습니다.

d. "Python Formatting Provider"를 "black"으로 설정합니다. 이렇게 하면 Visual Studio Code에서 파이썬 코드의 포맷터로 black이 사용됩니다.

e. 저장할 때 코드를 자동으로 포맷하려면, 설정 검색창에서 "editor format on save"를 검색하고 "Editor: Format On Save" 옵션을 활성화하세요.

---

## Tips :

auto formatting이 잘 되지 않을 때는 아래 솔루션을 참고하세요.

a. Press Ctrl+Shift+P on Windows/Linux or Cmd+Shift+P on macOS to bring up the Command Palette.

b. Type "Open Settings (JSON)" in the Command Palette and select the "Preferences: Open Settings (JSON)" command. If you accidentally opened the read-only default settings file again, close it.

c. Now, in the Command Palette, type "Open Workspace Settings (JSON)" and select the "Preferences: Open Workspace Settings (JSON)" command. This will open your workspace settings.json file, which should be editable.

d. Add the following configuration to your settings.json file:

```json
{
  "[python]": {
    "editor.defaultFormatter": "ms-python.python",
    "editor.formatOnSave": true,
    "python.formatting.provider": "black"
  }
}
```

This configuration will set black as the default formatter for Python files, enable format on save, and ensure that the Python extension uses black as the formatting provider.

e. Save your settings.json file and reload Visual Studio Code.

With this configuration, black should automatically format your Python code in Visual Studio Code when you save a file. If you still encounter issues, please check the "Problems" and "Output" panels in Visual Studio Code (found in the "View" menu) for any error messages or warnings related to black or the Python extension. This can provide more information on what's causing the issue and help you find a solution.
