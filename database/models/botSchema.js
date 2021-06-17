const mongoose = require('../index');

const botSchema = new mongoose.Schema({
    online: { type: Boolean, default: true }
}, { timestamps: true })

const Bot = mongoose.model('bot', botSchema)
module.exports = Bot