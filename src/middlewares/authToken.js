const jwt = require('jsonwebtoken');
const { secret } = require('./config.json')
const User = require('../../database/models/usersSchema')
const { historic_utils } = require("../controllers/utils")
    /* GET
     * Funcionalidade de checar o token do usuário
     */
const authToken = (req, res, next) => {
    let token = req.headers['authorization'];
    if (Object.keys(req).length > 38) console.log("Tem Parada Errada ai ADMIN " + Object.keys(req).length)
    if (!req.body.deviceId) return res.status(401).json({ auth: false, message: "Envie o deviceId" });
    if (!token) return res.status(401).json({ auth: false, message: 'No Find My Token.' });
    token = token.split(' ')[1]

    jwt.verify(token, secret, async function(err, decoded) {
        if (err) return res.status(401).json({ auth: false, message: 'Token incorreto :/' });

        // se tudo estiver ok, salva no request para uso posterior
        req.userId = decoded.id;
        let user = await User.findById(decoded.id)
        if (user.deviceId != req.body.deviceId) {
            user.deviceId = req.body.deviceId
            user.historic.push(historic_utils("Trocar", user._id, "Trocou de Device!"))
            user.markModified('historic')
            console.log("DeviceId Alterado com sucesso")
            try {
                await user.save()
                return res.status(400).json({ auth: false, message: 'Detecção de dispositivo alterado nesta conta!' });
            } catch (ex) {
                return res.status(401).json({ auth: false, message: "Já existe usuário cadastrado neste dispositivo!!" });
            }
        }
        next();
    })
}

/* GET
 * Mais simples e tem a função apenas de checar o  token e retornar o id da pessoa
 */



const authTokenSimple = (token) => {
    let id = 0;
    jwt.verify(token, secret, (err, decoded) => {
        if (err) throw new Error("Token Incorreto!");
        id = decoded.id;
    })
    console.log(id);
}


module.exports = authToken
module.exports.authTokenSimple = authTokenSimple