var User = require('../../database/models/usersSchema')
var Point = require('../../database/models/pointsSchema')
var { historic_utils } = require('./utils')

module.exports = {
    data: async (req, res) => {
        const { deviceId } = req.body
        const id = req.userId
        let validPoint = true
        const user = await User.findOne({ _id: id })
        if (!user.registeredpoint) {
            validPoint = false;
            console.info("Usuário não possui ponto")
        } else {
            const point = await Point.findById(user.registeredpoint)
            let filtred = point.employee.filter(emp => emp.email == user.email)
            if (filtred.length == 0) console.error("Inconsistência nos dados!!! userID: " + user._id)
            else if (!(filtred[0].deviceId == user.deviceId)) console.log("Trocou de Dispositivo")
        }

        if (user.deviceId != deviceId) return res.status(401).json({ message: "Dispositivo não registrado com esta conta!" });
        const { email, name, plan, city, country, vtr, pointowner, historic, _id } = user
        res.status(200).json({ message: "Autenticado", result: { email, name, plan, city, country, vtr, pointowner, historic, deviceId, _id, validPoint } })
    },
    update: async (req, res) => {
        const id = req.userId
        const { name, password, city, country, vtr } = req.body
        try {
            const user = await User.findOne({ _id: id })
            if (user == []) return res.status(400).json({ message: "Usuário não encontrado!" })
            if (name) {
                user.historic.push(historic_utils(`Update name`, user._id, `from ${user.name} to ${name}`))
                user.name = name
            }
            if (password) {
                user.historic.push(historic_utils(`Update password`, user._id, `from ${user.password} to ${password}`))
                user.password = password
            }
            if (city) {
                user.historic.push(historic_utils(`Update city`, user._id, `from ${user.city} to ${city}`))
                user.city = city;
            }
            if (country) {
                user.historic.push(historic_utils(`Update country`, user._id, `from ${user.country} to ${country}`))
                user.country = country
            }
            if (vtr) {
                user.historic.push(historic_utils(`Update vtr`, user._id, `from ${user.vtr} to ${vtr}`))
                user.vtr = vtr
            }
            user.markModified('historic');
            user.save()
            res.status(200).json({ message: "Update realizado com sucesso!" })
        } catch (err) {
            res.status(400).json({ message: "Cadastro não alterado alterado!", err })
        }

    }
}