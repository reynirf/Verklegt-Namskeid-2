# Castle Apartments

Castle Apartments is a Python library for dealing with word pluralization.

## Installation

[pip3](https://pip.pypa.io/en/stable/), [python3](https://www.python.org/downloads/) and [postgresSQL (version 11 is recommended)](https://www.postgresql.org/download/) are required for the project to run

### Mac

```bash
git clone https://github.com/reynirf/Verklegt-Namskeid-2.git
```
```bash
cd Verklegt-Namskeid-2
```

```bash
pip install virtualenv
```

```bash
virtualenv -p python ve-castle
```

```bash
source ve-castle/bin/activate
```

```bash
export PATH=$PATH:/Library/PostgreSQL/11/bin # (replace "11" with your postgresSQL version)
```

```bash
pip install -r requirements.txt
```

```bash
cd Castle
```

```bash
python manage.py runserver
```
#### Go to [http://127.0.0.0.1:8000/](http://127.0.0.0.1:8000/)

### Windows

```bash
git clone https://github.com/reynirf/Verklegt-Namskeid-2.git
```
```bash
cd Verklegt-Namskeid-2
```

```bash
pip install virtualenv
```

```bash
virtualenv -p python ve-castle
```

```bash
source ve-castle/Scripts/activate
```

```bash
pip install -r requirements.txt
```

```bash
cd Castle
```

```bash
python manage.py runserver
```
#### Go to [http://127.0.0.0.1:8000/](http://127.0.0.0.1:8000/)

## Contributors
- [Reynir](https://github.com/reynirf)
- [Guðrún](https://github.com/ithil13)
- [Sigurður](https://github.com/Siggso)
- [Viðar](https://github.com/viddi7)

