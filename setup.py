from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

version = {}
with open("vidstab/version.py") as f:
    exec(f.read(), version)

setup(name='vidstab',
      version=version['__version__'],
      description='Video Stabilization using OpenCV',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Adam',
      author_email='author@gmail.com',
      url='https://github.com/pi2017/python_video_stab',
      packages=['vidstab'],
      license='MIT',
      install_requires=[
          'numpy',
          'pandas',
          'imutils>=0.5.2',
          'progress',
          'matplotlib',
      ],
      extras_require={
          'cv2': ['opencv-contrib-python >= 3.4.0']
      },
      tests_require=['pytest'],
      keywords=['video stabilization', 'computer vision', 'image processing', 'opencv'],
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ]
      )
