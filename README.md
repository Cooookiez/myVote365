# 🗳 myVote365

## 💡 Assumptions

1. **Platforma do głosowania na zadane przez mówcy/wykładowcę/prelegenta pytania, np:**
   - "Czy się podobało?" [Tak/Nie]
   - "Jakie są szanse, że polecisz wykład?" [slider od 1 do 5]
   - "Co byś zmienił?" [Pole tekstowe]
2. **Widzowie mogą zeskanować kod qr / wpisać w przeglądarce link (np. myVote365.com/7HC0) i odpowiada na pytania.** (w jak najbardziej prosty dla nich sposób (Brak wymogu logowania dla nich i ¿inne?))
3. **Będzie działało na [django](https://www.djangoproject.com/) + [google firebase](https://firebase.google.com/).**

## Raport II

Lista zrobionych rzeczy jest w [To Do List](#-to-do-list)

Video podglądowe co jest już zrobione:

[![myVote365 – youtube video – raport II](http://img.youtube.com/vi/hm9VYDDarjA/0.jpg)](http://www.youtube.com/watch?v=hm9VYDDarjA)

## 📝 To Do List

- [x] [LOGIN & REGISTER] – **REGISTER**
  - [x] google reCAPTCHA
- [x] [LOGIN & REGISTER] – **LOGIN**
- [ ] [LOGIN & REGISTER] – **if wrong email, wrong error**
- [ ] [LOGIN & REGISTER] – **live check if email exist**
- [ ] [LOGIN & REGISTER] – "Co Najmniej 1 znak specjalny (!, @, #, $, …)" **Done, to delete❗️**
- [x] [PANEL] – **Settings**
  - [x] change name
  - [x] change email
  - [x] change password
- [x] [PANEL] – logout
- [ ] [PANEL] – **hide / extend left menu**
- [ ] [PANEL] – **footer with alpha looking bad when something is scrollable in main**
- [x] [SLIDE EDIT] – **Shows slide properties, after click on one**
- [x] [SLIDE EDIT] – **Update project title**
- [x] [SLIDE EDIT] – **Update slide properties**
  - [x] title
  - [x] type
  - [x] position
  - [x] max and min position input
- [x] [SLIDE EDIT] – **Update lecture properties**
  - [x] title
  - [x] position
  - [x] max and min position input
- [x] [SLIDE EDIT] – **Update status**
- [x] [SLIDE EDIT] – **Add/Remove lectures**
  - [x] Add
  - [x] Remove
- [x] [SLIDE EDIT] – **Add/Remove slides**
  - [x] Add
  - [x] Remove
- [x] [SLIDE EDIT] – **scrolable slides/lectures left panel**
- [ ] [SLIDE EDIT] – **slide preview**
- [ ] [SLIDE EDIT] – **With Add/Remove change active slide/lecture properties edit**
- [x] [PRESENTATION] – **start**
- [ ] [PRESENTATION] – **UI**
  - [x] footer
  - [x] qr section
  - [ ] slide section
- [ ] [PRESENTATION] – **qr slide❓**
- [ ] [PRESENTATION] – **other slides**
  - [ ] TAK / NIE
  - [ ] 1-2-3-4-5 (slider)
  - [ ] Text
- [ ] [PRESENTATION] – **is open** (so other can join to watch)

## 📆 Timetable

| Week (deadline)                       | Description                   | status |
| ------------------------------------: | ----------------------------- | :----: |
| 3 (12.03.2020)                        | Raport I (Project plan)       | ✅     |
| ~~8 (16.04.2020)~~<br>9 (23.04.2020)  | Raport II (Project status)    | ✅     |
| 11 (07.05.2020)                       | Prototype                     | 📝     |
| 13 (21.05.2020)                       | Raport III (Prototype update) | 🕐     |
| 14 (28.05.2020)                       | Submission of the project     | 🕒     |
| 15 (03.06.2020)                       | Project presentation          | 🕔     |

## 📚 Used libraries

- **[segno](https://pypi.org/project/segno/):** `pip install segno`
- **[bcrypt](https://pypi.org/project/bcrypt/):** `pip install bcrypt`
- **firebase-admin:**
  - **[github.com](https://github.com/firebase/firebase-admin-python):** `pip install firebase-admin`
  - **[firebase.google.com](https://firebase.google.com/docs/admin/setup/):** `sudo pip install firebase-admin`
- **[requests](https://pypi.org/project/bcrypt/):** `pip install requests`
