# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing module for `temp_file_tools.TemporaryFolder`.'''

import tempfile
import os.path
import pathlib

import nose.tools

import python_toolbox

from python_toolbox.temp_file_tools import TemporaryFolder


def test_basic():
    with TemporaryFolder() as tf1:
        assert isinstance(tf1, pathlib.Path)
        assert tf1.exists()
        assert tf1.is_dir()
        
        tf2 = TemporaryFolder()
        with tf2 as tf2:
            assert isinstance(tf2, pathlib.Path)
            assert tf2.exists()
            assert tf2.is_dir()
            
        assert not tf2.exists()
        assert not tf2.is_dir()
                
        assert tf1.exists()
        assert tf1.is_dir()
        file_path = (tf1 / 'my_file')
        with file_path.open('w') as my_file:
            my_file.write('Woo hoo!')
        
        assert file_path.exists()
        assert file_path.is_file()
        
        with file_path.open('r') as my_file:
            assert my_file.read() == 'Woo hoo!'
            
    assert not tf1.exists()
    assert not tf1.is_dir()
    
    assert not file_path.exists()
    assert not file_path.is_file()
    

def test_without_pathlib():
    with TemporaryFolder() as tf1:
        assert os.path.exists(str(tf1))
        assert os.path.isdir(str(tf1))
        
        tf2 = TemporaryFolder()
        with tf2 as tf2:
            assert os.path.exists(str(tf2))
            assert os.path.isdir(str(tf2))
            
        assert not os.path.exists(str(tf2))
        assert not os.path.isdir(str(tf2))
                
        assert os.path.exists(str(tf1))
        assert os.path.isdir(str(tf1))
        
        file_path = os.path.join(str(tf1), 'my_file')
        with open(file_path, 'w') as my_file:
            my_file.write('Woo hoo!')
        
        assert os.path.exists(file_path)
        assert os.path.isfile(file_path)
        
        with open(file_path, 'r') as my_file:
            assert my_file.read() == 'Woo hoo!'
            
    assert not os.path.exists(str(tf1))
    assert not os.path.isdir(str(tf1))
    
    assert not os.path.exists(file_path)
    assert not os.path.isdir(file_path)
    


def test_repr():
    tf = TemporaryFolder()
    assert '(Not created yet)' in repr(tf)
    with tf:
        assert '(Not created yet)' not in repr(tf)
        