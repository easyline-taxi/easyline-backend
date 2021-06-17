var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');
var cors = require('cors')
var logMiddleware = require('./middlewares/logIn');


var indexRouter = require('./routes/index');
var usersRouter = require('./routes/users');
var pointsRouter = require('./routes/points');
var plansRouter = require('./routes/plans');
var adminsuRouter = require('./routes/onlyAdmins');
var adminRouter = require('./routes/admin')
var botController = null;
// botController = require('./controllers/botController');

var app = express();

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'pug');

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(cors())
app.use(express.static(path.join(__dirname, 'public')));


app.use(logMiddleware)

// app.use(bot.middleware)

app.use('/', indexRouter);
app.use('/users', usersRouter);
app.use('/points', pointsRouter)
app.use('/plans', plansRouter)
app.use('/adminsu', adminsuRouter)
app.use('/admin', adminRouter)


// catch 404 and forward to error handler
app.use(function (req, res, next) {
  next(createError(404));
});

// error handler
app.use(function (err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;

  botController?.erroSend(err,req,res,next)

  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});




module.exports = app;


var routes = []
function print (path, layer) {
  if (layer.route) {
    layer.route.stack.forEach(print.bind(null, path.concat(split(layer.route.path))))
  } else if (layer.name === 'router' && layer.handle.stack) {
    layer.handle.stack.forEach(print.bind(null, path.concat(split(layer.regexp))))
  } else if (layer.method) {
    // console.log('%s /%s',
    //   layer.method.toUpperCase(),
    //   path.concat(split(layer.regexp)).filter(Boolean).join('/'))
      routes.push(`${layer.method.toUpperCase()} /${path.concat(split(layer.regexp)).filter(Boolean).join('/')}`)
      
  }
}

function split (thing) {
  if (typeof thing === 'string') {
    return thing.split('/')
  } else if (thing.fast_slash) {
    return ''
  } else {
    var match = thing.toString()
      .replace('\\/?', '')
      .replace('(?=\\/|$)', '$')
      .match(/^\/\^((?:\\[.*+?^${}()|[\]\\\/]|[^.*+?^${}()|[\]\\\/])*)\$\//)
    return match
      ? match[1].replace(/\\(.)/g, '$1').split('/')
      : '<complex:' + thing.toString() + '>'
  }
}
app._router.stack.forEach(print.bind(null, []))

botController?.bot.setRoutes(routes)