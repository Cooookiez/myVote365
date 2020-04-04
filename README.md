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
- [ ] [REGISTER & USER SETTINGS] – **"Co Najmniej 1 znak specjalny (!, @, #, $, …)" Zrobione ale usunąć❗️**
- [ ] [PANEL] – **hide / extend left menu**
- [ ] [PANEL] – **footer with alpha looking bad when something is scrollable in main**
- [ ] [LOGIN] – **if wrong email, wrong error**
- [x] [SLIDE EDIT] – **Pokazuje właściwości slajdu po naciśnieciu na jeden**
- [ ] [SLIDE EDIT] – **Updatuje tytuł projektu**
- [ ] [SLIDE EDIT] – **Wysyła zupdatowane właściwości slidu**

## 📆 Harmonogram

| tydzień         | nazwa                               | status |
| --------------: | ----------------------------------- | :----: |
| 3 (12.03.2020)  | Raport I (Plan projektu)            | ✅     |
| 8 (16.04.2020)  | Raport II (Stan projektu)           | 📝     |
| 11 (07.05.2020) | Prototyp                            | 🕐     |
| 13 (21.05.2020) | Raport III (Aktualizacja prototypu) | 🕒     |
| 14 (28.05.2020) | Oddanie projektu                    | 🕔     |
| 15 (03.06.2020) | Prezentacja projektu                | 🕖     |

## 📚 Used libraries

- **[segno](https://pypi.org/project/segno/):** `pip install segno`
- **[bcrypt](https://pypi.org/project/bcrypt/):** `pip install bcrypt`
- **firebase-admin:**
  - **[github.com](https://github.com/firebase/firebase-admin-python):** `pip install firebase-admin`
  - **[firebase.google.com](https://firebase.google.com/docs/admin/setup/):** `sudo pip install firebase-admin`
- **[requests](https://pypi.org/project/bcrypt/):** `pip install requests`
