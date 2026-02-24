---
name: til
description: 현재 세션에서 배운 내용을 TIL 볼트에 기록. 세션 내용을 분석하여 자동으로 태그와 내용을 생성.
user-invocable: true
---

# TIL 기록

이 세션에서 배운 핵심 내용을 TIL 노트로 작성하고, 관련 기초 지식 Concept 노트를 생성/연결한다.

## 폴더 구조

```
~/Documents/Obsidian/TIL/
├─ Entries/YYYY/YYYY-MM-DD.md   # 일별 TIL (배운 것 기록)
├─ Concepts/                     # 기초 지식 노트 (재사용 가능)
│   ├─ react-query-caching.md
│   ├─ error-boundary.md
│   └─ ...
└─ Templates/
    ├─ TIL.md
    └─ Concept.md
```

## 절차

### 1단계: TIL 엔트리 작성

1. 현재 세션의 대화를 분석하여 배운 점/핵심 내용을 파악
2. 적절한 태그를 자동 생성 (예: react, typescript, git, devops 등)
3. `~/Documents/Obsidian/TIL/Entries/YYYY/` 폴더에 `YYYY-MM-DD.md` 파일로 작성
4. 같은 날짜 파일이 이미 있으면 기존 내용 아래에 `---` 구분선 후 추가

### 2단계: Concept 노트 생성/연결

1. TIL에서 사용된 핵심 개념들을 추출 (예: keepPreviousData → "react-query-caching", useCallback → "react-memoization")
2. 각 개념에 대해 `~/Documents/Obsidian/TIL/Concepts/` 에 노트가 있는지 확인
3. **없으면 새로 생성**, **있으면 "관련 TIL" 백링크만 추가**
4. TIL 엔트리의 각 섹션에 `📚 [[concept-name]]` 링크를 추가

### Concept 노트 작성 규칙

- **파일명**: kebab-case 영어 (예: `react-query-caching.md`, `query-key-factory.md`)
- **깊이**: 핵심 개념 3-5줄 요약 + 코드 스니펫 1-2개 + 관련 TIL 백링크
- **누적형**: 이후 세션에서 같은 개념을 다루면 기존 노트에 내용 추가 (덮어쓰기 X)
- **연결**: 관련 Concept끼리도 `[[]]` 링크로 연결

## TIL 엔트리 형식

```markdown
---
date: "YYYY-MM-DD"
tags:
  - tag1
  - tag2
concepts:
  - "[[concept-1]]"
  - "[[concept-2]]"
---

# TIL - YYYY-MM-DD

## 배운 것

### 주제 1
(내용)
📚 [[관련-concept]]

### 주제 2
(내용)
📚 [[관련-concept]]

## 핵심 정리

(가장 중요한 포인트 1-3줄)

## 참고
- (관련 링크나 파일 경로)
```

## Concept 노트 형식

```markdown
---
aliases:
  - 한글 별칭
tags:
  - tag1
  - tag2
---

# Concept 제목

## 핵심 개념

(3-5줄 요약 — 이 개념이 무엇이고 왜 중요한지)

## 코드 예시

(핵심을 보여주는 최소 코드 스니펫 1-2개)

## 관련 개념
- [[다른-concept]]

## 관련 TIL
- [[YYYY-MM-DD]] — 어떤 맥락에서 사용했는지 한 줄
```

## 규칙
- 한국어로 작성
- 세션 전체를 요약하되 핵심만 간결하게
- 태그는 영어 소문자, 구체적으로 (예: `react-query` o, `frontend` x)
- 코드 스니펫이 있으면 포함
- Concept은 하나의 명확한 주제만 다룸 (너무 넓지 않게)
- Concept이 이미 존재하면 "관련 TIL" 섹션에 백링크만 추가하고, 내용이 보충될 때만 기존 내용에 추가
