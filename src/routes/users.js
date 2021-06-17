var express = require('express');
var routerUsers = express.Router();
var User = require('../../database/models/usersSchema')
var authControllers = require('../controllers/authController')
var userControllers = require('../controllers/userController')
var cache = require('../middlewares/memoryCache')
var authToken = require('../middlewares/authToken')



/* GET users listing. */
routerUsers.get('/', cache(10), function (req, res, next) {
  User.find().then((response) => {
    let final = []
    response.forEach((user) => {
      final.push({ nome: user.name, email: user.email, plan: user.plan })
    })
    res.json(final);
  })
});

routerUsers.post('/register', authControllers.register)
routerUsers.post('/login', authControllers.login)

routerUsers.use(authToken)
routerUsers.post('/data', userControllers.data)
routerUsers.post('/update', userControllers.update)



module.exports = routerUsers;
