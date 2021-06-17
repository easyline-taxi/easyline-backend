const Logs = require('../../database/models/logSchema')


const logIn = async (req, res, next) => {
        Logs.create({
            service: req.method,
            ip:req.headers.host,
            content:Object.keys(req.body).map(key => {return key+":"+(typeof req.body[key])}),
            params: req.params,
            target:req.originalUrl,
        })
    
    next();
}

module.exports = logIn