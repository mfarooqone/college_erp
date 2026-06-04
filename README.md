# Odoo 19 College ERP

[![License: LGPL-3](https://img.shields.io/badge/License-LGPL--3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)
[![Odoo](https://img.shields.io/badge/Odoo-19.0-875A7B.svg)](https://www.odoo.com)

**Odoo 19 Community addon** for college and institute management — student records, admissions, and education workflows.

Repository: [github.com/mfarooqone/odoo19_college_erp](https://github.com/mfarooqone/odoo19_college_erp)

---

## Features

- **Student registry** — Store name, admission number, admission date, gender, contact details, and address
- **Dedicated app** — *College ERP* appears in the Odoo app menu
- **List & form views** — Browse and manage students from the backend
- Built for **Odoo 19 Community Edition**

## Screenshots

_Add screenshots of the Students list and form views here._

---

## Requirements

| Component | Version |
|-----------|---------|
| Odoo | 19.0 (Community) |
| Python | 3.10 – 3.13 |
| PostgreSQL | 14+ |

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/mfarooqone/odoo19_college_erp.git
```

### 2. Add the module to your addons path

Copy the `college_erp` folder into your Odoo addons directory, **or** add this repository path to `addons_path` in `odoo.conf`:

```ini
addons_path = /path/to/odoo/addons,/path/to/odoo19_college_erp
```

Expected layout:

```text
odoo19_college_erp/
├── README.md
├── .gitignore
└── college_erp/          ← Odoo module (technical name)
    ├── __init__.py
    ├── __manifest__.py
    ├── models/
    └── views/
```

### 3. Install the module

**From the UI**

1. Restart Odoo
2. Enable **Developer mode** (*Settings → Activate the developer mode*)
3. Go to **Apps → Update Apps List**
4. Search **College ERP** → **Install**

**From the command line**

```bash
./odoo-bin -c odoo.conf -d YOUR_DATABASE -i college_erp --stop-after-init
```

### 4. Open the app

Go to **College ERP → Students Management** and create your first student.

---

## Configuration

No extra configuration is required after installation.

---

## Module structure

| Item | Value |
|------|--------|
| Technical name | `college_erp` |
| Main model | `college.students` |
| Depends on | `base` |
| License | LGPL-3 |

```text
college_erp/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── college_students.py
└── views/
    ├── college_students_views.xml
    └── college_erp_menus.xml
```

### Student fields

| Field | Type | Notes |
|-------|------|--------|
| `name` | Char | Required |
| `admission_number` | Char | Required |
| `admission_date` | Date | Required |
| `gender` | Selection | Male / Female |
| `email` | Char | |
| `phone` | Char | |
| `age` | Integer | |
| `address` | Text | |

---

## Roadmap

- [ ] Courses and programs
- [ ] Departments and faculty
- [ ] Fees and invoicing
- [ ] Attendance and timetables
- [ ] Reports and certificates

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -m "feat: add my feature"`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a Pull Request

---

## Author

**Najoom Al Thuraya**  
Website: [althurayauae.com](https://althurayauae.com/)

Maintainer: [@mfarooqone](https://github.com/mfarooqone)

---

## License

This project is licensed under the [GNU Lesser General Public License v3.0](https://www.gnu.org/licenses/lgpl-3.0.html) (LGPL-3), same as Odoo Community Edition.
