---
name: obsidian-issue
description: Use when creating or registering GitHub issues in the Work vault. Triggers on "이슈 등록", "이슈 만들어", or /obsidian-issue.
user-invocable: true
---

# 이슈 등록

GitHub 이슈를 Work 볼트의 Issue 폴더에 개별 노트로 생성한다.

## 절차

1. 사용자에게 필요한 정보를 확인 (이슈 번호, 제목, 프로젝트 등)
2. `~/Documents/Obsidian/Work/Issue/{이슈번호} - {제목}.md` 파일 생성
3. frontmatter와 본문 템플릿을 채워서 작성

## 필수 정보

| 항목 | 설명 | 기본값 |
|------|------|--------|
| issue_id | GitHub 이슈 번호 | (필수) |
| 제목 | 이슈 짧은 제목 | (필수) |
| project | 연결할 프로젝트 노트 이름 | (필수) |
| status | open / in-progress / done / wontfix | open |
| assignee | me / other / unassigned | me |
| priority | high / medium / low | medium |
| issue_url | GitHub 이슈 URL 또는 경로 | issues/{issue_id} |
| tags | 관련 태그 목록 | [] |

## 파일 형식

```markdown
---
issue_id:
status: open
assignee: me
priority: medium
project: "[[프로젝트명]]"
issue_url: ""
created: "YYYY-MM-DD"
resolved:
tags: []
---

## 증상

## 원인 분석

## 해결 방안

## 참고
```

## 규칙
- 한국어로 작성
- 파일명: `{이슈번호} - {짧은 제목}.md`
- 사용자가 증상/원인/해결방안을 알려주면 본문에 채워넣기
- 정보가 부족하면 빈 섹션으로 두기
- project는 `~/Documents/Obsidian/Work/Projects/` 내 기존 노트와 연결
