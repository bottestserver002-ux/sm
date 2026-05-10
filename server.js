const express = require("express");
const cors = require("cors");

const app = express();

app.use(cors());
app.use(express.json());

/* ======================
   DEMO DATABASE
====================== */

let poems = [
  {
    id: 1,
    title: "Bài thơ đầu tiên",
    content: "Nội dung bài thơ demo"
  }
];

let posts = [
  {
    id: 1,
    title: "Bài viết đầu tiên",
    content: "Nội dung bài viết demo"
  }
];

let users = [];

/* ======================
   ROUTES
====================== */

app.get("/poems", (req, res) => {
  res.json(poems);
});

app.get("/posts", (req, res) => {
  res.json(posts);
});

/* LOGIN */

app.post("/login", (req, res) => {
  const { email, password } = req.body;

  const user = users.find(
    u => u.email === email && u.password === password
  );

  if (!user) {
    return res.json({
      success: false,
      message: "Sai tài khoản hoặc mật khẩu"
    });
  }

  res.json({
    success: true,
    user
  });
});

/* REGISTER */

app.post("/register", (req, res) => {
  const { email, password } = req.body;

  const exists = users.find(u => u.email === email);

  if (exists) {
    return res.json({
      success: false,
      message: "Email đã tồn tại"
    });
  }

  const newUser = {
    id: Date.now(),
    email,
    password,
    role: "viewer"
  };

  users.push(newUser);

  res.json({
    success: true,
    user: newUser
  });
});

/* AI */

app.post("/ask-ai", (req, res) => {
  const { message } = req.body;

  res.json({
    reply: `AI trả lời: ${message}`
  });
});

/* ======================
   START
====================== */

app.listen(8000, () => {
  console.log("Server running http://localhost:8000");
});