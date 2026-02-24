---
name: work-log
description: 현재 세션의 작업 내용을 Work 볼트에 기록. 프로젝트 노트 업데이트 또는 새 항목 추가.
user-invocable: true
---

# 업무 기록

이 세션에서 수행한 작업을 Work 볼트에 정리한다.

## 절차

1. 세션에서 수행한 작업을 분석 (어떤 프로젝트, 뭘 했는지, 결과)
2. 해당 프로젝트 노트가 `~/Documents/Obsidian/Work/Projects/`에 있으면 업데이트
3. 없으면 새 프로젝트 노트 생성
4. 완료된 할일은 `- [x]`, 남은 것은 `- [ ]`로 표시

## 프로젝트 노트 형식

```markdown
---
status: active
created: "YYYY-MM-DD"
---

# 프로젝트명

## Goal
(프로젝트 목표)

## Tasks
- [x] 완료된 작업
- [ ] 남은 작업

## Notes
### YYYY-MM-DD
- 작업 내용 요약
```

## 규칙
- 한국어로 작성
- 기존 노트가 있으면 Notes 섹션에 날짜별로 추가
- status: `active`, `on-hold`, `done` 중 택1
- 할일은 구체적으로 (예: "로그인 API 연동" o, "작업" x)
