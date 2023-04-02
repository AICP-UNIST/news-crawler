# Pylint 설치하기

## 아직 가상 환경을 활성화하지 않았다면 지금 활성화하세요

Windows:

```
.venv\Scripts\activate
```

macOS와 Linux:

```
source .venv/bin/activate
```

## pip를 사용하여 pylint를 설치합니다

```
./pip_install.sh pylint
```

# Pylint 구성하기

프로젝트의 루트 디렉터리에 .pylintrc 파일을 생성하여 pylint 구성을 저장합니다.

다음 명령을 사용하여 기본 .pylintrc 파일을 생성합니다:

```
pylint --generate-rcfile > .pylintrc
```

.pylintrc 파일을 열고 필요에 따라 구성 옵션을 수정합니다. 일반적인 옵션에는 다음이 포함됩니다:

`max-line-length`: 단일 행에 허용되는 최대 문자 수를 설정합니다. 예: max-line-length=100
disable: 특정 규칙 또는 규칙 그룹을 비활성화합니다. 예: disable=missing-docstring,invalid-name
더 많은 구성 옵션은 Pylint 문서에서 찾을 수 있습니다.

# Visual Studio Code에서 Pylint 통합하기

a. Visual Studio Code에 Microsoft의 "Python" 확장 프로그램이 설치되어 있는지 확인합니다. 확장 뷰에서 (Ctrl+Shift+X 또는 Cmd+Shift+X 누르기) "Python"을 검색하여 찾을 수 있습니다.

b. 설정으로 이동하여 (왼쪽 하단의 톱니바퀴 아이콘을 클릭하고 "설정"을 선택합니다) Visual Studio Code가 기본 리터로 pylint를 사용하도록 구성합니다. 설정 검색 창에서 "python linting"을 입력하여 관련 설정을 찾습니다.

c. "Python Linting: Pylint Enabled" 옵션을 켜고, "Python Linting: Enabled" 옵션도 켜서 저장합니다.

이제 Visual Studio Code에서 Python 코드를 작성할 때 pylint가 자동으로 작동해야 합니다. 저장한 후에는 변경 사항이 적용되도록 Visual Studio Code를 새로 고칩니다.
