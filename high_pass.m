n=1
freq=10*2*pi;
fs=freq/(2*pi)
dt = 1/freq;

[b,a]=butter(n, 0.08,'high')

[h,f]=freqz(a,b,200,'whole',10); 
n=round(0.5*length(h));
f=(0:length(f)-1*fs/length(f));
plot(f(1:n)/fs,20*log10(abs(h((1:n)))))