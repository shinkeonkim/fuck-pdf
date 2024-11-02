# Fuck PDF

> PDF 편집 기능을 제공하는 GUI 프로그램

## 제공 기능 목록

- PDF 병합 기능
- PDF 페이지 삭제 기능
- 홀수 페이지 / 짝수 페이지 PDF 파일 병합 기능
- PDF 페이지 회전 기능

## Development / Debug

```bash
> poetry install
> poetry run pre-commit install
> poetry run python main.py
```

```bash
> pyinstaller --noconfirm --onefile --windowed --add-data "app:app" --icon=icon.icns --name=fuck_pdf app/main.py
```
