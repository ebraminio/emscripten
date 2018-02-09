import os, shutil, logging, subprocess

TAG = '1.7.5'

def get(ports, settings, shared):
  if settings.USE_HARFBUZZ == 1:
    ports.fetch_project('harfbuzz', 'https://github.com/harfbuzz/harfbuzz/releases/download/' +
      TAG + '/harfbuzz-' + TAG + '.tar.bz2', 'harfbuzz-' + TAG, is_tarbz2=True)
    def create():
      logging.info('building port: harfbuzz')
      ports.clear_project_build('harfbuzz')

      source_path = os.path.join(ports.get_dir(), 'harfbuzz', 'harfbuzz-' + TAG)
      dest_path = os.path.join(ports.get_build_dir(), 'harfbuzz')

      shutil.rmtree(dest_path, ignore_errors=True)

      shared.Building.configure(['cmake', '-H' + source_path, '-B' + dest_path, '-DCMAKE_BUILD_TYPE=Release'])
      subprocess.check_call(['make'], cwd=dest_path)
      return os.path.join(dest_path, 'libharfbuzz.a')
    return [shared.Cache.get('harfbuzz', create, what='port')]
  else:
    return []


def process_dependencies(settings):
  #TODO: Enable hb-ft dependency and add -DHB_HAVE_FREETYPE=ON to cmake configuration
  #if settings.USE_HARFBUZZ == 1:
  #  settings.USE_FREETYPE = 1
  pass

def process_args(ports, args, settings, shared):
  if settings.USE_HARFBUZZ == 1:
    get(ports, settings, shared)
    args += ['-Xclang', '-isystem' + os.path.join(ports.get_build_dir(), 'harfbuzz')]
  return args

def show():
  return 'harfbuzz (USE_HARFBUZZ=1; MIT license)'
