const express = require('express');
const session = require('express-session');
const cookieParser = require('cookie-parser');
const uuid = require('uuid');
const app = express();
const port = 3000;

app.use(cookieParser());

app.use(session({
  secret: 'your-secret-key',
  resave: false,
  saveUninitialized: true
}));

app.use(express.urlencoded({ extended: false }));

app.get('/', (req, res) => {
    if(!req.session.userId){
        req.session.userId = uuid.v4();
        console.log('New User, Session Created, ID: ' + req.session.userId);
    } else {
        console.log('Previous User, Session Restored, ID: ' + req.session.userId);
    }
    res.send('Main Page');
});

app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
