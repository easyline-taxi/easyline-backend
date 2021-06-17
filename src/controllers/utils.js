const db = require('../../database/index')

module.exports = {
    /**
     * 
     * @param {String} action 
     * @param {ObjectID} id 
     * @param {String} motive 
     * @returns 
     */
    historic_utils: (action, id, motive) => {
        return { action, id: id, motive, date: new Date() }
    },
    /**
     * 
     * @param {ObjectID} id 
     * @param {String} name 
     * @param {String} email 
     * @param {Number} vtr 
     * @param {ObjectID} deviceId 
     * @param {String} func 
     * @returns 
     */
    add_employee: (id, name, email, vtr, deviceId, func = "motorista") => {
        return { id: db.Types.ObjectId(id), name, email, vtr, deviceId, function: func }
    }, sleep: (ms) => {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

}