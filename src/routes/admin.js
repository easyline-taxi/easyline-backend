var express = require('express');
var router = express.Router();
var pointControllers = require('./../controllers/pointController')
var authToken = require('./../middlewares/authToken')
var adminCheck = require('./../middlewares/adminCheck')

router.use(authToken) //check auth

router.use(adminCheck) //check admin

router.post('/pa', ()=>{});

router.post('/manned', ()=>{});

router.post('/payments', ()=>{});

router.post('/location', ()=>{});

router.post('/users', ()=>{});

router.post('/users/banir', ()=>{});

router.post('/users/delete', ()=>{});

router.post('/users/add', ()=>{});

router.post('/users/transferir', ()=>{});

router.get('/plans', ()=>{});

router.post('/plans', ()=>{});

module.exports = router;