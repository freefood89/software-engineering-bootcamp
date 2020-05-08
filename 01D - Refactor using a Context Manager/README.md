# 01D - Refactor using a Context Manager

In this step you will improve your worker code's loop using a Context Manager [[docs](https://docs.python.org/3/reference/datamodel.html#context-managers)].

## More on Context Managers

As you may have seen in the offical python documentation, you've probably already used the following Context Manager:

```python
with open('hello.txt') as infile:
	some_text = infile.read() # the context
```

This code accomplishes the same thing as the following abbreviated snippet:

```python
infile = open('hello.txt')
try:
	some_text = infile.read() # the context
finally:
	infile.close()
```

The context created with the `with` statement guarantees that `infile.close()` is executed upon exiting. Without it, your computer can actually run out of file descriptors which are a shared resource used by all applications to point to files among other things. For example, some versions of Mac OS has a limit of 65536 file descriptors. 

Conveniently, a Context Manager can be implemented to catch exceptions thrown in the context. Returning to the `open()` example, according to this [Python tutorial](https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files):

> It is good practice to use the with keyword when dealing with file objects. The advantage is that the file is properly closed after its suite finishes, even if an exception is raised at some point. Using with is also much shorter than writing equivalent try-finally blocks

## Challenge

Create a Context Manager for SQS messages so that when the block is exited with no exceptions the message is automatically deleted from the SQS queue. If an exception is thrown in the block, the message should not be deleted from the SQS queue.

```python
while True:
	try:
		with sqs_queue.get() as message:
			# Do stuff with message
			# If exited without exception delete SQS message
	except ExpectedException as e:
		# handle exception and continue polling
```

