---
name: til
description: 현재 세션에서 배운 내용을 TIL 볼트에 기록. 세션 내용을 분석하여 자동으로 태그와 내용을 생성.
user-invocable: true
---

# TIL 기록

이 세션에서 배운 핵심 내용을 TIL 노트로 작성한다.

## 절차

1. 현재 세션의 대화를 분석하여 배운 점/핵심 내용을 파악
2. 적절한 태그를 자동 생성 (예: react, typescript, git, devops 등)
3. `~/Documents/Obsidian/TIL/Entries/YYYY/` 폴더에 `YYYY-MM-DD.md` 파일로 작성
4. 같은 날짜 파일이 이미 있으면 기존 내용 아래에 `---` 구분선 후 추가

## 파일 형식

```markdown
---
date: "YYYY-MM-DD"
tags:
  - tag1
  - tag2
---

# TIL - YYYY-MM-DD

## 배운 것

(세션에서 배운 핵심 내용을 간결하게 정리)

## 핵심 정리

(가장 중요한 포인트 1-3줄)

## 참고
- (관련 링크나 파일 경로)
```

## 규칙
- 한국어로 작성
- 세션 전체를 요약하되 핵심만 간결하게
- 태그는 영어 소문자, 구체적으로 (예: `react` o, `frontend` x)
- 코드 스니펫이 있으면 포함
