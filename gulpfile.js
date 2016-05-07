// grab our packages
var   gulp        = require('gulp');
      gutil       = require('gulp-util');
      sourcemaps  = require('gulp-sourcemaps');
      concat      = require('gulp-concat');
      gutil       = require('gulp-util');
      uglify      = require('gulp-uglify');

gulp.task('build-js', function() {
   return gulp.src('src/client/modules/*.js')
      .pipe(sourcemaps.init())
      .pipe(concat('scripts.min.js'))
      //only uglify if gulp is ran with '--type production'
      .pipe(gutil.env.type === 'production' ? uglify().on('error', gutil.log) : gutil.noop())
      .pipe(sourcemaps.write())
      .pipe(gulp.dest('src/client/content'));
});
