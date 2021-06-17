const User = require('../../database/models/usersSchema')
const adminCheck = async (req, res, next) => {
  const id  = req.userId
  if(!req.userId) res.status(401).json({message:'Aqui Você não tem poder'})
  let response = await User.findOne({ _id: id })
  if (!response?.pointowner) return res.status(401).json({ message: "Você não é Admin" })
    console.log("é Admin")
    req.userData = response
    next();
}

module.exports = adminCheck