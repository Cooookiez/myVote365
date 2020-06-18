# 🗳 myVote365

![fulfilled the assumptions](https://img.shields.io/badge/Fulfilled_assumptions-100%25-brightgreen)
![Raports](https://img.shields.io/badge/Raports_%26%20Presentation-100%25-blue)
![Version](https://img.shields.io/badge/Version-Alpha_v1.0-blueviolet)

## 💡 Assumptions

1. **Platforma do głosowania na zadane przez mówcy/wykładowcę/prelegenta pytania, np:**
   - "Czy się podobało?" [Tak/Nie]
   - "Jakie są szanse, że polecisz wykład?" [slider od 1 do 5]
   - "Co byś zmienił?" [Pole tekstowe]
2. **Widzowie mogą zeskanować kod qr / wpisać w przeglądarce link (np. myVote365.com/7HC0) i odpowiada na pytania.** (w jak najbardziej prosty dla nich sposób (Brak wymogu logowania dla nich i ¿inne?))
3. **Będzie działało na [django](https://www.djangoproject.com/) + [google firebase](https://firebase.google.com/).**

## Raports

### Raport II

Lista zrobionych rzeczy jest w [To Do List](#-to-do-list)

Video podglądowe co jest już zrobione:

[![myVote365 – youtube video – raport II](http://img.youtube.com/vi/hm9VYDDarjA/0.jpg)](http://www.youtube.com/watch?v=hm9VYDDarjA)

### Raport III

Od prototypu dodałem podgląd slajdu (na razie “tak / nie”) oraz odpowiedzi dla niego, plus sporo poprawek i usprawnień

![slide yes / no](README_media/Raport%20III/raport-iii-phone-desktop.png)

### Oddanie projektu

Dokończyłem resztę slidów aby był podgląd podczas pokazu

![slide slider 1 to 5](README_media/Oddanie%20projektu/oddanie_slider_1to5.png)
![slide text](README_media/Oddanie%20projektu/oddanie_text.png)

Oraz podczas edytowania (tutaj jest podgląd z defaultowymi danymi)
![panel](README_media/Oddanie%20projektu/oddanie%202.png)

## 📝 To Do List

- [x] [LOGIN & REGISTER] – **REGISTER**
  - [x] google reCAPTCHA
- [x] [LOGIN & REGISTER] – **LOGIN**
- [x] [PANEL] – **Settings**
  - [x] change name
  - [x] change email
  - [x] change password
- [x] [PANEL] – logout
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
- [x] [SLIDE EDIT] – **slide preview**
- [x] [PRESENTATION] – **start**
- [x] [PRESENTATION] – **UI**
  - [x] footer
  - [x] qr section
  - [x] slide section
- [x] [PRESENTATION] – **other slides**
  - [x] TAK / NIE
  - [x] 1-2-3-4-5 (slider)
  - [x] Text
- [x] [PRESENTATION] – **is open** (so other can join to watch)
- [x] [PRESENTATION] – **sent data** (for spectators)
- [x] [PRESENTATION] – **recive views**
- [x] [SPECTATOR] – **Front page** (to write id)
- [x] [SPECTATOR] – **Active presentation page** (with following slide no)
- [x] [SPECTATOR] – **slide page**
  - [x] TAK / NIE
  - [x] 1-2-3-4-5 (slider)
  - [x] Text
- [x] [SPECTATOR] – **Send views**
- [x] [SPECTATOR] – **inactiv presentation ...**

## 📆 Timetable

| deadline   | Description                   | status |
| ---------: | ----------------------------- | :----: |
| 12.03.2020 | Raport I (Project plan)       |   ✅   |
| 23.04.2020 | Raport II (Project status)    |   ✅   |
| 21.05.2020 | Prototype                     |   ✅   |
| 28.05.2020 | Raport III (Prototype update) |   ✅   |
| 04.06.2020 | Submission of the project     |   ✅   |
| 18.06.2020 | Project presentation          |   ✅   |

## 📚 Used libraries

- **[segno](https://pypi.org/project/segno/):** `pip install segno`
- **[bcrypt](https://pypi.org/project/bcrypt/):** `pip install bcrypt`
- **firebase-admin:**
  - **[github.com](https://github.com/firebase/firebase-admin-python):** `pip install firebase-admin`
  - **[firebase.google.com](https://firebase.google.com/docs/admin/setup/):** `sudo pip install firebase-admin`
- **[requests](https://pypi.org/project/bcrypt/):** `pip install requests`
