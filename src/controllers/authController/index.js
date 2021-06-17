var User = require('../../../database/models/usersSchema')
var Point = require('../../../database/models/pointsSchema')
const bcrypt = require('bcrypt');
const saltRounds = 12;
const { secret } = require('../../middlewares/config.json');
const {bot} = require('../botController')
const db = require('../../../database/index')
const { historic_utils, add_employee } = require('../utils')


const jwt = require('jsonwebtoken');

/*
 * Requisição deve conter no mínimo:  
    email: { type: String, unique: true, required: true },
    deviceId: { type: String, unique: true, required: true},
    nome: {type:String, required: true},
    password: {type:String,required: true},
*/
module.exports = {
    register: async (req, res, next) => {
        let { email, deviceId, name, password, city, country, vtr, admin } = req.body
        if (req.body.password) {
            const hash = bcrypt.hashSync(password, saltRounds);
            password = hash
        }
        let user;
        let ponto;
        try {
            if (admin == true) {
                if (req.body.nameofpoint) {
                    ponto = await Point.find({ name: req.body.nameofpoint })
                    if (ponto.length > 0) return res.status(400).json({ message: "Nome do ponto já existe" })
                    user = await User.create({ email, deviceId, name, password, city, country, vtr })
                    ponto = await Point.create({ name: req.body.nameofpoint, plan: db.Types.ObjectId("6050d657e5757a23046d0070"), owner: db.Types.ObjectId(user._id) })
                    user.pointowner = db.Types.ObjectId(ponto._id)
                    user.historic.push(historic_utils(`${ponto.name} - Ponto Criado `, ponto._id, "Fundador"))
                    user.markModified('historic')

                    ponto.historic.push(historic_utils(`${user.name} - Entrou no ponto`, user._id, "Fundador"))
                    ponto.employee.push(add_employee(user._id, user.name, user.email, user.vtr,user.deviceId, "admin"))
                    ponto.markModified('employee')
                    ponto.markModified('historic')
                    if (ponto == [] || ponto == null || user == null || user == []) {
                        User.deleteOne(user)
                        Point.deleteOne(ponto)
                        return res.status(400).json({ message: "Houver Inconsistência no cadastro de admin" })
                    }
                    await ponto.save()
                    await user.save()
                } else return res.status(400).json({ message: "Nome do ponto é Necessário!" })

            } else user = await User.create({ email, deviceId, name, password, city, country, vtr })


            // bot.sendMessage({ title: "Cadastrado com Sucesso", content: `Usuário: ${user.email}` })

            res.status(200).json({ message: "Usuário Cadastrado com Sucesso" })

        } catch (error) {
            if (user) User.findOneAndDelete({ _id: user._id })
            if (ponto) Point.findOneAndDelete({ _id: ponto._id })
            res.status(400).json({ message: "Não Houve Sucesso no Cadastro!",error })
        }

    },
    login: async (req, res, next) => {
        const { email, password, deviceId } = req.body

        const user = await User.findOne({ email })
        if (user.length == 0) return res.status(404).json({ message: "Login não Encontrado" })
        bcrypt.compare(password, user.password, function (err, result) {
            if (err) return res.status(401).json("Falha no login")
            if (result) {

                const token = jwt.sign({ id: user._id }, secret, {
                    expiresIn: 60 * 60 * 24 * 4 // expires in 4 dias
                });
                bot.sendMessage({ title: "Logado com Sucesso", content: `Usuário: ${user.email}` })
                return res.status(200).json({ message: "Logado com Sucesso", token })
            } else {
                return res.status(401).json({ message: "password ou Email incorretos" })
            }

        });

    }
}