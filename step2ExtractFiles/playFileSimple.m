function playFileSimple(myfile)

    [y,Fs] = wavread(myfile);
    
    obj1 = audioplayer(y, Fs);
    obj1.TimerFcn = 'showSeconds';
    obj1.TimerPeriod = 1;
    
    playblocking(obj1);
end

function showSeconds
    disp('tick');
end