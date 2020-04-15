# 🗳 myVote365

## 💡 Assumptions

1. **Platforma do głosowania na zadane przez mówcy/wykładowcę/prelegenta pytania, np:**
   - "Czy się podobało?" [Tak/Nie]
   - "Jakie są szanse, że polecisz wykład?" [slider od 1 do 5]
   - "Co byś zmienił?" [Pole tekstowe]
2. **Widzowie mogą zeskanować kod qr / wpisać w przeglądarce link (np. myVote365.com/7HC0) i odpowiada na pytania.** (w jak najbardziej prosty dla nich sposób (Brak wymogu logowania dla nich i ¿inne?))
3. **Będzie działało na [django](https://www.djangoproject.com/) + [google firebase](https://firebase.google.com/).**

## 📝 To Do List (for now)

- [ ] [REGISTER & USER SETTINGS] – **update hints**
- [ ] [REGISTER & USER SETTINGS] – **live check if email exist**
- [ ] [REGISTER & USER SETTINGS] – "Co Najmniej 1 znak specjalny (!, @, #, $, …)" **Done, to delete❗️**
- [ ] [PANEL] – **hide / extend left menu**
- [ ] [PANEL] – **footer with alpha looking bad when something is scrollable in main**
- [ ] [LOGIN] – **if wrong email, wrong error**
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
- [ ] [SLIDE EDIT] – **scrolable slides/lectures left panel**
- [ ] [SLIDE EDIT] – **slide preview**
- [ ] [SLIDE EDIT] – **With Add/Remove change active slide/lecture properties edit**
- [ ] [PRESENTATION] – **start**

## 📆 Timetable

| Week (deadline) | Description                   | status |
| --------------: | ----------------------------- | :----: |
| 3 (12.03.2020)  | Raport I (Project plan)       | ✅     |
| 8 (16.04.2020)  | Raport II (Project status)    | 📝     |
| 11 (07.05.2020) | Prototype                     | 🕐     |
| 13 (21.05.2020) | Raport III (Prototype update) | 🕒     |
| 14 (28.05.2020) | Submission of the project     | 🕔     |
| 15 (03.06.2020) | Project presentation          | 🕖     |

## 📚 Used libraries

- **[segno](https://pypi.org/project/segno/):** `pip install segno`
- **[bcrypt](https://pypi.org/project/bcrypt/):** `pip install bcrypt`
- **firebase-admin:**
  - **[github.com](https://github.com/firebase/firebase-admin-python):** `pip install firebase-admin`
  - **[firebase.google.com](https://firebase.google.com/docs/admin/setup/):** `sudo pip install firebase-admin`
- **[requests](https://pypi.org/project/bcrypt/):** `pip install requests`
