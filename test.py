from boto3 import resource
from boto3.dynamodb.conditions import Attr, Key

demoTable = resource("dynamodb").Table("TiktokReddit")
