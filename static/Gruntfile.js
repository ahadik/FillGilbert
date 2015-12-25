module.exports = function(grunt) {
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),

    sass: {
      options: {
        includePaths: ['node_modules/foundation-sites/scss']
      },
      dist: {
        options: {
          outputStyle: 'nested'
        },
        files: {
          'css/app.css': 'scss/app.scss'
        }        
      },
    },
    jade: {
      compile: {
        options: {
          data: {
            debug: false
          },
          pretty: true
        },
        files: [{
          'expand': true,
          'cwd': 'src/',
          'src':["*.jade", "!_*.jade"],
          'ext': '.html'
        }] 
      }
    },
    watch: {
      grunt: { files: ['Gruntfile.js'] },

      sass: {
        files: 'scss/**/*.scss',
        tasks: ['sass', 'autoprefixer'],
        options: {
          livereload: true
        }
      },
      jade: {
        files: 'src/*.jade',
        tasks: ['jade'],
        options: {
          livereload: true
        }
      }
    },
      autoprefixer: {
        dist: {
            files: {
                'css/app.css': 'css/app.css'
            }
        }
      }
  });

  grunt.loadNpmTasks('grunt-sass');
  grunt.loadNpmTasks('grunt-contrib-jade');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks ('grunt-autoprefixer');
  grunt.loadNpmTasks('grunt-newer');

  grunt.registerTask('build', ['sass']);
  grunt.registerTask('default', ['build','watch']);
}