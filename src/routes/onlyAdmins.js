var express = require('express');
var router = express.Router();
const basicAuth = require('express-basic-auth')

var User = require('../../database/models/usersSchema')
var Plan = require('../../database/models/plansSchema')
var Point = require('../../database/models/pointsSchema')

const pointController = require('../controllers/pointController');

router.use(basicAuth({
    users: { 'admin': 'superadmin' }
}))

router.get('/deleteall', async function (req, res, next) {
    try {
        await User.deleteMany({})
        // await Plan.deleteMany({})
        await Point.deleteMany({})
        res.status(200).json({ message: "Banco Deletado" })
    } catch (err) {
        res.status(400).json({ message: "Não deletados" })
    }
});

router.get('/inconsistencias', pointController.findInconsistences);



module.exports = router;