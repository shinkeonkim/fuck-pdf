# Fuck PDF

> PDF 편집 기능을 제공하는 GUI 프로그램

## 제공 기능 목록

- PDF 병합 기능
- PDF 페이지 삭제 기능
- 홀수 페이지 / 짝수 페이지 PDF 파일 병합 기능
- PDF 페이지 회전 기능

### PDF 병합 기능

<img width="500" alt="image" src="https://github.com/user-attachments/assets/208d5fec-df6b-4d2b-8f9d-25a373efa91e">

- 여러 PDF 파일을 불러올 수 있습니다.
- PDF 파일의 순서를 조정하고, 병합하여 파일을 저장할 수 있습니다.

### PDF 페이지 삭제 기능

<img width="500" alt="image" src="https://github.com/user-attachments/assets/9b82051c-29f3-4c5f-9c02-53d77d78dec8">

- PDF 파일을 불러올 수 있습니다.
- 특정 페이지를 선택하고 삭제한 후, 파일을 저장할 수 있습니다.

### 홀수 페이지 / 짝수 페이지 PDF 파일 병합 기능

<img width="500" alt="image" src="https://github.com/user-attachments/assets/91b97f1d-9b2a-4938-bf51-748b3f5af074">

- 두 PDF 파일을 번갈아가며 병합할 수 있습니다.
  - ex) 양면 스캔이 지원되지 않는 스캐너에서 파일을 각각 스캔 후, 파일을 병합할 수 있습니다.

### PDF 페이지 회전 기능

<img width="500" alt="image" src="https://github.com/user-attachments/assets/9492b368-2dc7-4864-865f-d152a9f0ff25">

- PDF 파일을 불러올 수 있습니다.
- 각 페이지마다 90도 단위로 회전시킬 수 있습니다.

## Development / Debug

```bash
> poetry install
> poetry run pre-commit install
> poetry run python main.py
```

```bash
> pyinstaller --noconfirm --onefile --windowed --add-data "app:app" --icon=icon.icns --name=fuck_pdf app/main.py
```
