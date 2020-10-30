clear all
load('Hqp');
load('f');
load('Aqp');
load('bqp');
load('Aeq');
load('beq');
load('ub');
load('lb');

f = double(f);
python()

z = quadprog(Hqp,f,Aqp,bqp,Aeq,beq,lb,ub)