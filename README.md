# mima - My Image App

## Installation

1. Create virtual environment.
```bash
python3 -m venv mima-venv && source mima-env/bin/activate
```
2. Clone the repository.
```bash
git https://github.com/Bhupesh-V/mima
```
3. Install Dependencies.
```bash
pip3 install -r requirements.txt
```
4. Create `.env` file. Go to Developer Settings on [imagekit](imagekit.io) to get your private & public key.
```txt
FLASK_APP=app.py
FLASK_ENV=development
TEMPLATES_AUTO_RELOAD = True
IMAGEKIT_PRIVATE_KEY=<PASTE-PRIVATE-KEY-HERE>
IMAGEKIT_PUBLIC_KEY=<PASTE-PUBLIC-KEY-HERE>
URL_ENDPOINT=https://ik.imagekit.io/bhupesh
```
5. Run Flask development server
```bash
flask run
```

## Author

👥 **Bhupesh Varshney**

- Twitter: [@bhupeshimself](https://twitter.com/bhupeshimself)
- DEV: [bhupesh](https://dev.to/bhupesh)

[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
