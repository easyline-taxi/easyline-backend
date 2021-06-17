var express = require('express');
var router = express.Router();
var Logs = require('../../database/models/logSchema')

/* GET home page. */
router.get('/', function (req, res, next) {
  res.render('index', { title: 'Express' });
});

// router.post('/testService', (req, res) => {
//   const body = JSON.stringify(req.body);
//   console.log("ip de acesso: " + req.headers['x-forwarded-for'] || req.connection.remoteAddress)
//   const last = new Logs({ service: "post", ip: req.headers['x-forwarded-for'] || req.connection.remoteAddress, content: body })
//   last.save((err, res) => { console.log(err) })

//   res.sendStatus(200).json({ message: "success" })
// })


// router.get('/testservice/:service', async (req, res, next) => {
//   console.log(req.params.service)
//   if (req.params.service) {
//     await Logs.find({ service: req.params.service })
//       .then((logs) => res.render("tests_post", { body: logs }))
//       .catch((err) => console.log(err))
//   } else {
//     await Logs.find()
//       .then((logs) => res.render("tests_post", { body: logs }))
//       .catch((err) => console.log(err))
//   }

// })

// router.get('/testservice', (req, res, next) => {

//   Logs.find()
//     .then((logs) => res.render("tests_post", { body: logs }))
//     .catch((err) => console.log(err))

// })

module.exports = router;
