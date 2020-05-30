# Romeo Tensorflow Installation

## Quickstart

This quickstart assumes you have done all the steps discussed throughout
the document (this includes setting up your bashrc files, and installing
tensorflow). We include it here so you have an easy way to remember once
you have set up your environment how to start a notebook.

Once you have set up the environment as discussed previously you need 3 terminals

* terminal 1: ```r-allocate```
* terminal 2: ```r-jupyter```
* terminal 3: ```r-port file:// ....``` # copy the line from terminal 2 with the file://
* browser: copy the url with local host in it in your browser

You will see the jupyter notebook


## Account

* Make sure you get a futuresystems account on
  <https://futuresystems.org>. You will have to declare a project you
  work on with us. Often this is created by the faculty member,
  not the students.
* Make sure you have created an ssh key with `ssh-keygen` in a
  shell. On Windows use gitbash and install it the default way on your
  machine. Linux and macOS have the ssh commands build in
* Upload the public key in `~/.ssh/id_rsa.pub` into the public key
  field whne going to your futuresystems account and edit it. The
  account information link is placed on the bottom of the page
* Now you have to wait a while till your key gets populated to juliet
  and romeo. This is a process done automatically every 10 minutes, but
  a system administrator has to activate your account which requires
  sending a help ticket

## Setup

The setup is a bit complex, follow the instructions carefully. We assume
you use bash, zsh, or gitbash (in case of Windows). Other shells are not  
discussed here.

## Host machine setup

Place the following in your .bashrc, or .zprofile or .pash_profile
(depends on your computer):

```
# ##############################################
# BEGIN ROMEO SETUP
# ##############################################
# chose your own favourite port and host 
JPORT="9100"
JHOST="r-003"
JLOG="${HOME}/log-juliet-jupyter.txt"
JMOUNT="${HOME}/DESKTOP"
JUSER="<Your FutureSystems User Name on Juliet>"
juliet="${JUSER}@juliet.futuresystems.org"
# its in dir juliet, please create it first

# FUNTIONS
function r-port {
    RPORT=`grep "file:" ${JLOG}`
    ssh -L ${JPORT}:r-003:${JPORT} -i ${RPORT} ${juliet}
}

function r-open {
    RHTML=`grep "127." ${JLOG} | tail -1 | sed 's/or //g'`
    echo
    echo ${RHTML}
    echo
    /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome "${RHTML}"
}

alias r-allocate='ssh ${juliet} "salloc -p romeo --reservation=lijguo_11"'
alias r-install='ssh -t ${juliet} "ssh r-003 \"curl -Ls http://cloudmesh.github.io/get/romeo/tf | sh\""'
alias romeo='ssh -t ${juliet} "ssh ${JHOST}"'

alias r='ssh -t ${juliet} "ssh ${JHOST}"'
alias j='ssh ${juliet}'

function r-start-jupyter {
    echo "pkill -u ${JUSER} jupyter-lab; ~/ENV3/bin/jupyter-lab --port ${JPORT} --ip 0.0.0.0 --no-browser" | ssh ${juliet} "ssh ${JHOST}"
}

alias r-ps='echo "ps -aux| fgrep ${JUSER}" | ssh juliet "ssh ${JHOST}"'
alias r-kill='echo "echo; hostname; echo; pkill -u ${JUSER} jupyter-lab" | ssh ${juliet} "ssh ${JHOST}"'

function r-jupyter {
    rm -f ${JLOG}
    r-start-jupyter 2>&1 | tee ${JLOG}
}

alias j-mount="cd ${JMOUNT}; sshfs ${juliet}:shared ${juliet} -o auto_cache ; cd ${JMOUNT}/${juliet}"
alias j-umount="cd ${JMOUNT}; umount ${juliet}"

alias p-mount="cd ${HOME}; sshfs ${juliet}:ENV3 RPYTHON -o auto_cache"
alias p-umount="cd ${HOME}; umount RPYTHON"

# ##############################################
# END ROMEO SETUP
# ##############################################
```


This provides the following commands to you

* `r-allocate`

  to get an allocation, call once. When you close the window the
  allocation is terminated and none of the commands will work well

* `r-install`

  Tensorflow software stack installation in your home dir on romeo ~/ENV3

  You have to do this only once

* `r`

  This logs you into romeo

* `j`

  This logs you into juliet

* `r-ps`

  This dos a ps on romeo

* `r-kill`

  This kills all jupyter processes on romeo

* `r-jupyter`

  This starts a jupyter lab notebook

  To use it you need to call in a new window after you copy the line with
  file:// in it

  ```r-port file://....```

  This will establish a connection to the notebook

  Next, you can pates and copy the line with http:// and local host into your browser

## Setup `.bashrc` on juliet

On juliet you must include the following in your bashrc file

```
if ! [ "$HOSTNAME" = j-login1 ]; then
    VCUDA=10.1
    VCUDNN=v7.6.5

    VMODULE=10.1-${VCUDNN}
    module load cuda/${VCUDA}
    module load cudnn/${VMODULE}
    export CUDNN_INCLUDE_DIR=/opt/cudnn-${VCUDA}-linux-x64-${VCUDNN}/cuda/include/
    export CUDNN_LIB_DIR=/opt/cudnn-${VCUDA}-linux-x64-${VCUDNN}/cuda/lib64/
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda-${VCUDA}/extras/CUPTI/lib64

fi



```

## SSHFS

Sometimes it is beneficial to use your local browsers to access files
on romeo. We do this at this time just via juliet and anable sharing
with sshfs. This tool is avialable for many OSes and you need to install
it before using.

Gregor has placed the following additional lines in hos. bashrc file on
his local computer:

```
alias j-mount="cd ${HOME}/Desktop; sshfs juliet:shared juliet -o auto_cache ; cd ${HOME}/Desktop/juliet"
alias j-umount="cd ${HOME}/Desktop; umount juliet"

```

Once you say j-mount it mounts the dir juliet:~/share to a local
directory ~/Desktop/juliet. As the files on juliet are shared with romeo
they are available also there.

In the terminal you simply can say

```j-mount``` for mount and
```j-unmount`` for ummounting.





## Using Romeo

To login you can now say

```bash
r
```

## Check GPU Availability

To check the availability of the GPU's say

```bash
nvidia-smi
```

## Test Script

To test if this all works, please copy the following into a notebook  
and execute

```python
import os
import warnings
import tensorflow as tf
import logging

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=FutureWarning)

logging.getLogger('tensorflow').setLevel(logging.FATAL)

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

if tf.test.is_gpu_available():
    print("------------------------------")
    print("GPU AVAILABLE")
    names = tf.test.gpu_device_name()
    print("------------------------------")
    print("GPU Device Names")
    print(names)

```

The output of the code looks like

```
---
GPU AVAILABLE
------------------------------
GPU Device Names
/device:GPU:0
```

## GPU Test Code

This test code may run for a long time, so you may want to interrupt
it after a while. It will put some load on the CUDA Cards and if you
use `nvidia-smi` you will see the load reported.

```
git clone git@github.com:vibhatha/mpi4tf.git
pip3 install mpi4tf
cd mpi4tf
python3 examples/model_parallel/model_parallel_v2.py
```

A convenient way to watch the changing load is to use in another
terminal to use the watch command

```bash
$ watch -n 5 nvidia-smi
```

This will repeat the monitor every 5 seconds. Please make sure you
kill this program and do not run it continuously as the `nvidia-smi`
program creates unnecessary load if not absolutely needed


## Extended GPU Setup On Romeo for Pytorch

Using Pytorch to do distributed training with MPI backend is
documented here

* <https://github.com/vibhatha/PytorchExamples>

