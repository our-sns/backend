🎇 backend

<br>

# 🛠 <span style="color: #0000FF">나만의 SNS 만들기</span>

<br>

## 🤝<span style="color: #00B050">프로젝트 팀 편성</span>

🙋‍♀️ Front-end : 송희연

> - github : https://github.com/songhuiyeon99

🙋‍♂️ Back-end : 최선우

> - github : https://github.com/25th-Night
> - blog : https://velog.io/@brown_eyed87

<br>

## 🖼 <span style="color: #00B050">프로젝트 주제 : 나만의 SNS 만들기</span>

이미지 삽입 (instagram_attach)

<br>

## 📌 <span style="color: #00B050">기능 구현 목표</span>

### 🎁 <span style='background-color: #ffffe8'>1차 구현 목표</span>

- 회원가입/로그인 기능 (jwt 활용)
- 글쓰기 기능
- 특정한 글에 대한 댓글 기능
- 특정한 글에 대한 좋아요 기능

<br>

### 🎁 <span style='background-color: #ffffe8'>2차 구현 목표</span>

- 내 정보 및 내가 쓴 글 / 내가 좋아요 누른 글만 모아보는 기능
- 유저 / 글 검색 기능
- (옵션) 특정 유저에 대한 팔로우 / 팔로잉 기능
- (옵션) 특정 유저와의 채팅

<br>

## 📖 요구사항 정의

### 🎆 <span style='background-color: #ffffe8'>Front-End</span>

#### 📑 <span style='background-color: #faf1f5'>필수 요구 사항</span>

**1-1**. 글 / 유저 / 댓글 등의 정보는 모두 `백엔드와의 통신`을 통해서 받아와야 합니다.

(axios 활용, 혹은 rtk query 나 react query 사용 권장)

**1-2.** 글쓰기 / 댓글 달기 / 좋아요 기능도 모두 `백엔드와의 통신`을 통해서 구현되어야 합니다.

(ex. 글쓰기 버튼 누르면, post 요청을 통해서 백엔드에 등록되도록)

**2**. 회원가입 / 로그인 기능은 JWT 토큰을 활용하도록 구현

**3.** 게시글 컴포넌트에 좋아요 등록/해제를 위한 버튼을 만들고, 좋아요 등록 여부에 따라 버튼의 형태가 달라지도록 구현

(ex. 좋아요된 글은 꽉 찬 하트, 좋아요되지 않은 글은 빈 하트)

**4.** 유저 검색, 글 검색 기능 구현 (인스타처럼 @, # 등으로 구분해서 검색 가능하도록 할 필요없으며,

어떤 기준으로 검색할지 유저가 선택한 후에 검색하도록 구현하는 것을 권장)

**5.** 내 정보 및 내가 쓴 글 / 내가 좋아요 누른 글만 모아보는 기능 구현

**6.** 전체 피드 보기 / 검색 결과 보기 / 내 정보 및 게시글 보기를 전환할 수 있도록 화면 하단에 탭 컴포넌트 제작

**7.** 전체 피드 보기 / 검색 결과 보기 / 내 정보 및 게시글 보기 페이지 각각 구현

(react-router-dom 활용)

**8.** redux 를 통해서 상태 관리 (유저 정보 등)

> **1회성으로 사용되는 상태라면 굳이 redux로 관리하지 않아도 무방합니다.**

#### 📄 <span style='background-color: #faf1f5'>선택 요구 사항</span>

**1.** (옵션) useCallback, useMemo 등을 통한 컴포넌트 렌더링 최적화

**2.**(옵션) 채팅 기능을 백엔드와 협업해서 구현

**3.**(옵션) 팔로우/팔로잉 기능을 백엔드와 협업해서 구현

<br>

### 🎇 <span style='background-color: #ffffe8'>Back-End</span>

#### 📑 <span style='background-color: #faf1f5'>필수 요구 사항</span>

**0.** 프론트엔드에서 요청을 보낼 수 있도록 aws 를 통한 배포 (cors 설정 필수)

**1.** 회원가입 / 로그인 기능은 JWT 토큰을 활용해서 토큰을 리턴하도록 구현

**2.** 글쓰기 / 댓글 달기 (글과 댓글을 Foreign Key로 연결) / 좋아요 (글과 유저를 Foreign Key로 연결) 기능 구현

**3.** 유저 및 글 검색 기능 구현 (검색은 url parameter 로 구현: Get 요청이어야함)

**4.** 유저 정보 및 유저가 쓴 글 혹은 좋아요 누른 글 리턴하도록 구현 (serializer 활용)

#### 📄 <span style='background-color: #faf1f5'>선택 요구 사항</span>

**1.** (옵션) 채팅 기능 구현 (django channels 등 활용)

**2.** (옵션) 팔로우/팔로잉 기능 구현 (follow 테이블 추가)

**3.** (옵션) aws rds 를 통해서 db 서버 활용해보기

**4.** (옵션) 사진 업로드의 경우, s3 를 통해서 구현해보기

<br>

## ✨ <span style="color: #00B050">평가 기준</span>

- [<span style="color: red">**공통**</span>] <span style="color: #B8860B">**로그인**</span> : 로그인 요청을 보내면 응답으로 JWT token 을 받아 쿠키/세션으로 set 하는 과정을 구현했다.
- [<span style="color: red">**공통**</span>] <span style="color: #B8860B">**회원가입**</span> : 회원가입 요청을 보내면 응답으로 JWT token 을 받아 쿠키/세션으로 set 하는 과정을 구현했다.
- [<span style="color: red">**공통**</span>] <span style="color: #B8860B">**글**</span> : 글에 대한 Post 요청 (글쓰기) 을 보내면 db 에 글이 추가되는 과정을 구현했다.
- [<span style="color: red">**공통**</span>] <span style="color: #B8860B">**글**</span> : 글에 대한 Get 요청을 보내면 db 에 있는 글 (+ 댓글) 을 가져와 사용자에게 보여주는 과정을 구현했다.
- [<span style="color: red">**공통**</span>] <span style="color: #B8860B">**댓글**</span> : 댓글에 대한 Post 요청 (댓글쓰기) 을 보내면 db 에 (특정 글과 연결된) 댓글이 추가되는 과정을 구현했다.
- [<span style="color: red">**공통**</span>] <span style="color: #B8860B">**좋아요**</span> : 글에 대한 좋아요 요청 (Post) 을 보내면 db 에 (특정 글에 대한 좋아요 수가) 반영되도록 구현했다.
- [<span style="color: red">**공통**</span>] <span style="color: #B8860B">**검색**</span> : 글/유저에 대한 검색 요청 (Get)을 보내면 해당 검색 조건을 만족한 결과만 db 에서 가져와 사용자에게 보여주는 과정
- [<span style="color: red">**FE**</span>] <span style="color: #B8860B">**화면 전환**</span> : react-router-dom 을 활용해서 전체 피드 보기 / 글쓰기 / 마이페이지 등을 전환할 수 있도록 구현했다.
- [<span style="color: red">**FE**</span>] <span style="color: #B8860B">**버튼 표시**</span> : 좋아요 여부에 따라 좋아요 버튼의 표시가 달라지도록 구현했다.
- [<span style="color: red">**BE**</span>] <span style="color: #B8860B">**모델 구현**</span> : 글, 댓글, 유저 모델을 Foreign Key 를 사용해서 연결되도록 구현했다.
