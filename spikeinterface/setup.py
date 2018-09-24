import setuptools

pkg_name="spikeinterface"

setuptools.setup(
    name=pkg_name,
    version="0.1.0",
    author="Cole Hurwitz, Jeremy Magland, Alessio Paolo Buccino, Matthias Hennig",
    author_email="colehurwitz@gmail.com",
    description="Python interface to spike sorting input and output file formats",
    url="",
    packages=setuptools.find_packages(),
    package_data={},
    install_requires=[
        'numpy',
        'quantities',
        'mountainlab_pytools',
        'neo'
    ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    )
)
