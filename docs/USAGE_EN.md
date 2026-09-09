# How to use FastMock (Guide for Frontend & Mobile Developers)

If the backend isn't ready yet, but you need to build UI, render lists, handle network errors, or plot real-time charts — **FastMock** will save your time. You don't need to know Python or databases to run it.

---

## 🛠 Step 1: Start the server (Takes 1 minute)

You don't need to configure environments. Everything works via Docker.

1. Ensure you have [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed.
2. Download this project (or run `git clone`).
3. Open a terminal in the project folder and type:
   ```bash
   docker compose up
   ```
4. Done! The server is running. Open the dashboard in your browser: **http://127.0.0.1:8000/docs**

---

## 📄 Step 2: Add API Contracts (Swagger)

FastMock doesn't know in advance which endpoints your app needs. You have to provide a specification (OpenAPI / Swagger file).

1. Ask your backend developer for the `openapi.yaml` file (or write a simple one yourself).
2. Go to the dashboard (http://127.0.0.1:8000/docs).
3. Find the green **`POST /_admin/specs`** button, click *Try it out*, select your file, and hit *Execute*.
4. **Magic:** The server instantly generates all the endpoints defined in the file!

> 💡 **Quick Start:** There is an `openapi.example.yaml` file in the project folder. Just copy it, rename it to `openapi.yaml`, and restart the server. You'll instantly get working `/users` and `/products` endpoints.

---

## 📱 Step 3: Connect your application

Now, simply change the base URL in your iOS/Android/Web app's code to `http://127.0.0.1:8000`.

### 🧠 Smart Data Generation
Make a `GET /users` request from your app. You won't get an empty response. FastMock will generate realistic JSON! If a field is named `email`, it returns a real random email; if it's `id`, it generates a UUID.

### 💾 Data Persistence (Forms)
Want to test a profile creation form?
1. Send a `POST /users` from your app with any JSON (e.g., `{"name": "John"}`).
2. Make a `GET /users` request. John will appear in the list!
The data is saved. *(Note: if you start the server with the `--persist db.json` flag, data is saved to a file that you can edit right in your text editor!)*

---

## 🌩 Step 4: Testing Errors (Chaos Engineering)

How will your app behave if the user has a poor 3G connection in the subway, or the backend crashes with a 500 error?
You don't need to unplug your ethernet cable! Just add Headers to your requests from the app:

* `X-Mock-Delay: 2000` — The server will "think" for exactly 2 seconds before responding. Check your loading spinners!
* `X-Mock-Status: 500` — The server will forcibly return a 500 Server Error. Test your error alerts and fallback screens!

---

## ⏱ Step 5: WebSockets Testing (Real-time)

If you're building a chat or a crypto chart, you need WebSockets. FastMock can simulate those too!

Connect your app to `ws://127.0.0.1:8000/ws/chat`.
1. **Echo:** Send any text, and it comes right back.
2. **Data Stream:** Send a special JSON `{"action": "stream", "interval": 1}`, and the server will infinitely stream new generated data to you every second! (Send `{"action": "stop"}` to pause it).

Happy coding! 🚀
