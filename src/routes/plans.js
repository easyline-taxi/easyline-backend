var express = require('express');
var router = express.Router();
var Plans = require('../../database/models/plansSchema')
const basicAuth = require('express-basic-auth')


router.get('/', async (req, res) => {
  let result = await Plans.find()
  res.status(200).json(result)
})

router.use(basicAuth({
  users: { 'admin': 'superadmin' }
}))

router.post('/create', async (req, res, next) => {
  try {
    await Plans.create(req.body)
    res.status(200).json({ message: "Criado Plano com sucesso" })
  } catch (err) {
    res.status(400).json({ message: "Plano não criado", erro: err })
  }
});

module.exports = router;
