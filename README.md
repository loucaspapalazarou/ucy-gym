# UCY Gym Automatic Reservations

#### Instructions

##### 1. Install dependencies
```bash
pip install -r requirements.txt
```

##### 2. Create your `.env`
```bash
cp .env.example .env
```

##### 3. Add your credentials in `.env`

```
GYM_USERNAME=<your-email>
GYM_PASSWORD=<your-password>
```

#### Execution

- ##### Run now
```bash
python main.py
```

- ##### Scedule run every day at 00:10
```bash
python main.py -s
```