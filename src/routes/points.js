var express = require('express');
var router = express.Router();
var pointControllers = require('../controllers/pointController')
var authToken = require('../middlewares/authToken')
var adminCheck = require('../middlewares/adminCheck')


//apenas autenticados 
router.use(authToken)

router.post('/create',pointControllers.newPoint)

//admins
router.use(adminCheck)

router.post('/change',pointControllers.changeOwner)
router.post('/delete',pointControllers.deletePoint)
router.post('/useradd', pointControllers.userAdd)
router.post('/userdel', pointControllers.userDel)



module.exports =router
