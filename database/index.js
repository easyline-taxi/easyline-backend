const mongoose = require('mongoose');

mongoose.connect('mongodb+srv://easyline:6&s1SfNgtR1y@cluster0.pfbkd.mongodb.net/easyline?authSource=admin&replicaSet=atlas-b54j3e-shard-0&w=majority&readPreference=primary&appname=MongoDB%20Compass%20Community&retryWrites=true&ssl=true', { useNewUrlParser: true})
    .then(() => console.log("Connection sucessfully established"))
    .catch(() => console.log("Connection Failed"));
mongoose.set('useCreateIndex', true);
// mongoose.set('useUnifiedTopology',true)
mongoose.Promise = global.Promise;
module.exports = mongoose;
