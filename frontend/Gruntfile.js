module.exports = function(grunt) {

  require('load-grunt-tasks')(grunt);

  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),

    bower_concat: {
      all: {
        dest: {
          js: 'dist/assets/js/vendor.js',
          css: 'build/assets/css/vendor.css',
          scss: 'build/assets/css/vendor.scss'
        }
      }
    },

    // concat: {
    //   dist: {
    //     src: ['app/**/*.js'],
    //     dest: 'build/assets/js/latitude.js'
    //   }
    // },

    // handlebarsify: {
    //   compile: {
    //     files: {
    //       'build/assets/js/templates.js': 'app/templates/**/*.hbs'
    //     }
    //   }
    // },

    browserify: {
      options: {
        browserifyOptions: { debug: true }
      },
      dist: {
        options: {
          transform: [["babelify", { presets: 'es2015', sourceMaps: 'inline' }], ['hbsfy']]
        },
        files: {
          'dist/assets/js/latitude.js': 'app/app.js'
        }
      }
    },
    //
    // babel: {
    //   options: {
    //     sourceMap: true,
    //     plugins: ['transform-es2015-modules-amd'],
    //     presets: ['es2015']
    //   },
    //   dist: {
    //     files: [
    //       { expand: true, cwd: 'app/', src: ["**/*.js"], dest: 'build/' }
    //       // 'dist/assets/js/latitude.js': 'app/app.js' //'build/assets/js/latitude.js'
    //     ]
    //   }
    // },

    concat: {
      dist: {
        src: ['build/assets/js/*.js'],
        dest: 'dist/assets/js/latitude.js'
      }
    },

    sass: {
      options: { sourceMap: true },
      dist: {
        files: {
          'dist/assets/css/vendor.css': ['build/assets/css/vendor.scss', 'build/assets/css/vendor.css'],
          'dist/assets/css/latitude.css': 'src/styles/app.scss'
        }
      }
    },

    copy: {
      main: {
        files: [
          { src: 'app/index.html', dest: 'dist/index.html' },
          { expand: true, src: ['app/public/**'], dest: 'dist/' }
        ]
      }
    },

    watch: {
      scripts: {
        files: ['app/**/*.*'],
        tasks: ['browserify', 'sass', 'copy']
      }
    },

    connect: {
      server: {
        options: {
          port: 4201,
          livereload: true,
          base: 'dist/'
        }
      }
    },

    clean: ['dist/', 'build/']
  });

  grunt.registerTask('build', ['bower_concat', 'browserify', 'sass', 'copy']);
  grunt.registerTask('default', ['build']);
  grunt.registerTask('serve', ['build', 'connect', 'watch']);

}
